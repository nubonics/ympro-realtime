import asyncio
import logging
import os
import json
import hashlib
from typing import Callable, Awaitable, List, Dict, Set, Optional

import httpx
from redis.asyncio import Redis

from backend.polling.models import Task, Hostler, PollResult
from backend.deps import REDIS_URL
from backend.rules.validation import validate_and_fix_tasks, check_task_rules
from backend.storage import set_latest_poll_result

POLL_INTERVAL_DEFAULT = int(os.getenv("POLL_INTERVAL", "10"))  # seconds
BASE_URL = os.getenv("POLLER_URL", "http://localhost:9000")
AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH", "./poller_audit.log")
RECENT_DELETIONS_CACHE_SIZE = 500

logger = logging.getLogger("poller")
logging.basicConfig(level=logging.INFO)


def hash_result(result: PollResult) -> str:
    """Hash the poll result for change detection."""
    as_bytes = json.dumps(result.model_dump(), sort_keys=True).encode("utf-8")
    return hashlib.sha256(as_bytes).hexdigest()


async def fetch_workbasket(client: httpx.AsyncClient) -> List[Task]:
    resp = await client.get(f"{BASE_URL}/workbasket")
    resp.raise_for_status()
    return [Task(**t) for t in resp.json()["tasks"]]


async def fetch_hostlers_summary(client: httpx.AsyncClient) -> List[dict]:
    resp = await client.get(f"{BASE_URL}/hostlers/summary")
    resp.raise_for_status()
    return resp.json()["hostlers"]


async def fetch_hostler_details(client: httpx.AsyncClient, hostler_id: str) -> List[Task]:
    resp = await client.get(f"{BASE_URL}/hostlers/{hostler_id}/details")
    resp.raise_for_status()
    tasks = resp.json().get("tasks", [])
    if not isinstance(tasks, list):
        logger.warning(f"Expected a list of tasks for hostler {hostler_id}, got: {type(tasks)}")
        tasks = []
    return [Task(**t) for t in tasks]


def audit_log(event: str, task: Task, reason: Optional[str] = None):
    """Append an audit log entry to the log file."""
    entry = {
        "event": event,
        "task_id": getattr(task, "id", None),
        "assigned_to": getattr(task, "assigned_to", None),
        "type": getattr(task, "type", None),
        "door": getattr(task, "door", None),
        "trailer": getattr(task, "trailer", None),
        "reason": reason,
        "timestamp": asyncio.get_event_loop().time()
    }
    try:
        with open(AUDIT_LOG_PATH, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        logger.error(f"Failed to write audit log: {e}")


async def delete_external_task(client: httpx.AsyncClient, task_id: str, recent_deletions: Set[str],
                               max_retries: int = 3):
    """Idempotently delete a task from the external API, with retries and caching."""
    if task_id in recent_deletions:
        logger.info(f"Task {task_id} was recently deleted, skipping redundant DELETE.")
        return
    for attempt in range(1, max_retries + 1):
        try:
            resp = await client.delete(f"{BASE_URL}/tasks/{task_id}")
            if resp.status_code in (200, 204, 404):  # 404 means already gone
                logger.info(f"Deleted invalid external task {task_id} (attempt {attempt})")
                recent_deletions.add(task_id)
                # Maintain cache size
                if len(recent_deletions) > RECENT_DELETIONS_CACHE_SIZE:
                    recent_deletions.pop()
                return
            else:
                logger.warning(f"Failed to delete task {task_id}: HTTP {resp.status_code}")
        except Exception as e:
            logger.error(f"Error deleting task {task_id} (attempt {attempt}): {e}")
        await asyncio.sleep(2 ** attempt)  # Exponential backoff


async def patch_external_task(client: httpx.AsyncClient, task: Task, patch_data: dict):
    """Try to patch/repair a fixable task in the external API."""
    try:
        resp = await client.patch(f"{BASE_URL}/tasks/{task.id}", json=patch_data)
        if resp.status_code in (200, 204):
            logger.info(f"Patched task {task.id} with {patch_data}")
            audit_log("patched", task, reason=f"Patched with {patch_data}")
            return True
        else:
            logger.warning(f"Failed to patch task {task.id}: HTTP {resp.status_code}")
    except Exception as e:
        logger.error(f"Error patching task {task.id}: {e}")
    return False


async def poll_forever(
        handle_payload: Callable[[PollResult, Redis], Awaitable[None]]
):
    """
    Periodically polls remote API, aggregates results, stores in Redis, and calls handle_payload.
    Only updates Redis/handlers on change.
    - Fetches all tasks (workbasket and all hostlers) in parallel.
    - Deduplicates and validates all tasks globally.
    - Splits by assigned_to (workbasket if None, hostler otherwise).
    - If a task fails validation, attempts to PATCH if fixable, otherwise DELETEs it from remote API.
    - Audit logs failures and deletions.
    - Tracks recently deleted task IDs to avoid redundant actions.
    - Poll interval is dynamically configurable via Redis key 'poll_interval', falls back to env/default.
    """
    redis = Redis.from_url(REDIS_URL, decode_responses=True)
    last_result_hash = None
    recent_deletions: Set[str] = set()
    async with httpx.AsyncClient() as client:
        while True:
            try:
                # -- Dynamic poll interval
                poll_interval = POLL_INTERVAL_DEFAULT
                try:
                    new_interval = await redis.get("poll_interval")
                    if new_interval:
                        poll_interval = int(new_interval)
                except Exception:
                    pass

                logger.info("Polling external system...")

                # -- Fetch all data concurrently
                workbasket_tasks_coro = fetch_workbasket(client)
                hostlers_raw = await fetch_hostlers_summary(client)
                # Fetch hostler tasks in parallel
                hostler_tasks_coros = [
                    fetch_hostler_details(client, h["id"]) for h in hostlers_raw
                ]
                workbasket_tasks, hostler_tasks_lists = await asyncio.gather(
                    workbasket_tasks_coro,
                    asyncio.gather(*hostler_tasks_coros)
                )
                all_hostler_tasks = [task for sublist in hostler_tasks_lists for task in sublist]

                # -- Combine all tasks for global deduplication and validation
                all_tasks = workbasket_tasks + all_hostler_tasks
                structurally_cleaned = validate_and_fix_tasks(all_tasks)

                # -- Apply business rules, PATCH fixable, DELETE unfixable
                valid_tasks = []
                invalid_tasks = []
                for t in structurally_cleaned:
                    allowed, reason, fix_data = check_task_rules(t, structurally_cleaned, return_patch_data=True)
                    if allowed:
                        valid_tasks.append(t)
                    elif fix_data:
                        logger.info(f"Attempting to patch task {t.id}: {fix_data}")
                        patched = await patch_external_task(client, t, fix_data)
                        if patched:
                            audit_log("patched", t, reason)
                        else:
                            audit_log("patch_failed", t, reason)
                            invalid_tasks.append((t, reason))
                    else:
                        invalid_tasks.append((t, reason))

                # -- Delete invalid tasks from external API and audit log them
                for t, reason in invalid_tasks:
                    logger.warning(f"Deleting task {t.id} due to failed business rules: {reason}")
                    audit_log("deleted", t, reason)
                    await delete_external_task(client, t.id, recent_deletions)

                # -- Split by assigned_to: None (workbasket) vs not None (hostler)
                final_workbasket = [t for t in valid_tasks if getattr(t, "assigned_to", None) is None]
                final_hostler_tasks = {h["id"]: [] for h in hostlers_raw}
                for t in valid_tasks:
                    hostler_id = getattr(t, "assigned_to", None)
                    if hostler_id:
                        final_hostler_tasks[hostler_id].append(t)

                # -- Build hostler details objects
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

                # -- Aggregate result
                result = PollResult(
                    workbasket_tasks=final_workbasket,
                    hostlers=hostler_details
                )

                # -- Only write to Redis/handlers if result changed
                result_hash = hash_result(result)
                if result_hash != last_result_hash:
                    logger.info("Poll result changed, updating Redis and invoking handlers.")
                    await set_latest_poll_result(result.model_dump(), redis)
                    await handle_payload(result, redis)
                    last_result_hash = result_hash
                else:
                    logger.info("Poll result unchanged, skipping Redis update.")

                # -- Metrics/logging: periodic summary
                logger.info(f"Polling cycle: {len(final_workbasket)} workbasket tasks, "
                            f"{sum(len(v) for v in final_hostler_tasks.values())} hostler tasks, "
                            f"{len(invalid_tasks)} deletions, "
                            f"poll interval={poll_interval}s")

            except Exception as e:
                logger.error(f"[Poller] Error: {e}")

            await asyncio.sleep(poll_interval)
