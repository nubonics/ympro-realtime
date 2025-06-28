import asyncio
import logging
import os
import time

import httpx
from redis.asyncio import Redis

from .models import Hostler, PollResult
from .api import ExternalApiClient
from .cache import TaskCache
from .audit import audit_log
from .utils import hash_result
from ..deps import REDIS_URL
from ..rules.validation import validate_and_fix_tasks, check_task_rules
from ..storage import set_latest_poll_result

POLL_INTERVAL_DEFAULT = int(os.getenv("POLL_INTERVAL", "10"))
BASE_URL = os.getenv("POLLER_URL", "http://localhost:9000")
RECENT_DELETIONS_CACHE_SIZE = 500
SEMAPHORE_LIMIT = 50  # Tune this based on your scaling/testing


async def delete_external_task(api, task_id, recent_deletions, cache, max_retries=3):
    my_logger = logging.getLogger("poller.delete_external_task")
    if task_id in recent_deletions:
        my_logger.info(f"Task {task_id} was recently deleted, skipping redundant DELETE.")
        return
    for attempt in range(1, max_retries + 1):
        try:
            deleted = await api.delete_task(task_id)
            if deleted:
                my_logger.info(f"Deleted invalid external task {task_id} (attempt {attempt})")
                recent_deletions.add(task_id)
                await cache.delete(task_id)
                if len(recent_deletions) > RECENT_DELETIONS_CACHE_SIZE:
                    recent_deletions.pop()
                return
            else:
                my_logger.warning(f"Failed to delete task {task_id}: not a valid status code")
        except Exception as e:
            my_logger.error(f"Error deleting task {task_id} (attempt {attempt}): {e}")
        await asyncio.sleep(2 ** attempt)


async def patch_external_task(api, task, patch_data, cache):
    my_logger = logging.getLogger("poller.patch_external_task")
    try:
        updated_details = await api.patch_task(task.id, patch_data)
        my_logger.info(f"Patched task {task.id} with {patch_data}")
        audit_log("patched", task, reason=f"Patched with {patch_data}")
        await cache.set(task.id, updated_details)
        return True
    except Exception as e:
        my_logger.error(f"Error patching task {task.id}: {e}")
    return False


async def fetch_and_cache_task_details(tasks, api, cache, semaphore_limit=SEMAPHORE_LIMIT):
    """
    Fetch task details concurrently with bounded concurrency and error handling.
    Logs cache hits, misses, and errors.
    """
    my_logger = logging.getLogger("poller.fetch_and_cache")
    semaphore = asyncio.BoundedSemaphore(semaphore_limit)

    async def get_and_update(t):
        async with semaphore:
            try:
                start = time.monotonic()
                details = await cache.get(t.id)
                if details:
                    my_logger.debug(f"Cache hit for task {t.id}")
                else:
                    my_logger.info(f"Cache miss for task {t.id}, fetching from API")
                    details = await api.fetch_task_details(t.id)
                    await cache.set(t.id, details)
                for k, v in details.items():
                    setattr(t, k, v)
                elapsed = time.monotonic() - start
                if elapsed > 2.0:
                    my_logger.warning(f"Fetching details for task {t.id} took {elapsed:.2f}s")
                return t
            except Exception as e:
                my_logger.error(f"Error fetching details for task {getattr(t, 'id', 'unknown')}: {e}")
                return None

    coros = [get_and_update(t) for t in tasks]
    results = await asyncio.gather(*coros)
    # Filter out any that failed
    return [t for t in results if t is not None]


async def poll_forever(handle_payload):
    my_logger = logging.getLogger("poller.poll_forever")
    redis = Redis.from_url(REDIS_URL, decode_responses=True)
    cache = TaskCache(redis)
    last_result_hash = None
    recent_deletions = set()
    async with httpx.AsyncClient() as http_client:
        api = ExternalApiClient(http_client, BASE_URL)
        while True:
            try:
                poll_interval = POLL_INTERVAL_DEFAULT
                try:
                    new_interval = await redis.get("poll_interval")
                    if new_interval:
                        poll_interval = int(new_interval)
                except Exception:
                    pass

                my_logger.info("Polling external system...")

                workbasket_tasks_coro = api.fetch_workbasket()
                hostlers_raw = await api.fetch_hostlers_summary()
                hostler_tasks_coros = [
                    api.fetch_hostler_details(h["id"]) for h in hostlers_raw
                ]
                workbasket_tasks, hostler_tasks_lists = await asyncio.gather(
                    workbasket_tasks_coro,
                    asyncio.gather(*hostler_tasks_coros)
                )
                all_hostler_tasks = [task for sublist in hostler_tasks_lists for task in sublist]

                all_tasks = workbasket_tasks + all_hostler_tasks
                detailed_tasks = await fetch_and_cache_task_details(all_tasks, api, cache)

                structurally_cleaned = validate_and_fix_tasks(detailed_tasks)

                valid_tasks = []
                invalid_tasks = []
                for t in structurally_cleaned:
                    allowed, reason, fix_data = check_task_rules(t, structurally_cleaned, return_patch_data=True)
                    if allowed:
                        valid_tasks.append(t)
                    elif fix_data:
                        my_logger.info(f"Attempting to patch task {t.id}: {fix_data}")
                        patched = await patch_external_task(api, t, fix_data, cache)
                        if patched:
                            audit_log("patched", t, reason)
                        else:
                            audit_log("patch_failed", t, reason)
                            invalid_tasks.append((t, reason))
                    else:
                        invalid_tasks.append((t, reason))

                for t, reason in invalid_tasks:
                    my_logger.warning(f"Deleting task {t.id} due to failed business rules: {reason}")
                    audit_log("deleted", t, reason)
                    await delete_external_task(api, t.id, recent_deletions, cache)

                final_workbasket = [t for t in valid_tasks if getattr(t, "assigned_to", None) is None]
                final_hostler_tasks = {h["id"]: [] for h in hostlers_raw}
                for t in valid_tasks:
                    hostler_id = getattr(t, "assigned_to", None)
                    if hostler_id:
                        final_hostler_tasks[hostler_id].append(t)

                hostler_details = {}
                for h in hostlers_raw:
                    h_id = h["id"]
                    hostler_details[h_id] = Hostler(
                        id=h_id,
                        name=h.get("name"),
                        checker_id=h.get("checker_id"),
                        moves=h.get("moves"),
                        tasks=final_hostler_tasks[h_id]
                    )

                result = PollResult(
                    workbasket_tasks=final_workbasket,
                    hostlers=hostler_details
                )

                result_hash = hash_result(result)
                if result_hash != last_result_hash:
                    my_logger.info("Poll result changed, updating Redis and invoking handlers.")
                    await set_latest_poll_result(result.model_dump(), redis)
                    await handle_payload(result, redis)
                    last_result_hash = result_hash
                else:
                    my_logger.info("Poll result unchanged, skipping Redis update.")

                my_logger.info(f"Polling cycle: {len(final_workbasket)} workbasket tasks, "
                               f"{sum(len(v) for v in final_hostler_tasks.values())} hostler tasks, "
                               f"{len(invalid_tasks)} deletions, "
                               f"poll interval={poll_interval}s")

            except Exception as e:
                my_logger.error(f"[Poller] Error: {e}")

            await asyncio.sleep(poll_interval)
