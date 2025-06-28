import os
import httpx
import asyncio
import logging
import json
from .models import Task, Hostler, PollResult
from .storage import get_redis  # Updated import

POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "10"))  # seconds
BASE_URL = os.getenv("POLLER_URL", "http://localhost:9000")

logger = logging.getLogger("poller")
logging.basicConfig(level=logging.INFO)


async def fetch_workbasket(client) -> list[Task]:
    resp = await client.get(f"{BASE_URL}/workbasket")
    resp.raise_for_status()
    return [Task(**t) for t in resp.json()["tasks"]]


async def fetch_hostlers_summary(client) -> list[dict]:
    resp = await client.get(f"{BASE_URL}/hostlers/summary")
    resp.raise_for_status()
    return resp.json()["hostlers"]


async def fetch_hostler_details(client, hostler_id: str) -> list[Task]:
    resp = await client.get(f"{BASE_URL}/hostlers/{hostler_id}/details")
    resp.raise_for_status()
    return [Task(**t) for t in resp.json()["tasks"]]


async def set_latest_poll_result(result: PollResult):
    """
    Store the latest poll result in Redis.
    """
    redis = await get_redis()
    # Convert the PollResult (with Hostler objects) to dict first if needed
    result_dict = {
        "workbasket_tasks": [t.dict() for t in result.workbasket_tasks],
        "hostlers": {hid: h.dict() for hid, h in result.hostlers.items()}
    }
    await redis.set("latest_poll_result", json.dumps(result_dict))
    await redis.close()


async def poll_forever(handle_payload):
    async with httpx.AsyncClient() as client:
        while True:
            try:
                logger.info("Polling external system...")
                # 1. Fetch unassigned tasks
                workbasket_tasks = await fetch_workbasket(client)

                # 2. Fetch hostler summary
                hostlers_raw = await fetch_hostlers_summary(client)

                # 3. For each hostler, fetch assigned tasks
                hostler_details = {}
                for h in hostlers_raw:
                    tasks = await fetch_hostler_details(client, h["id"])
                    hostler = Hostler(
                        id=h["id"],
                        name=h["name"],
                        checker_id=h["checker_id"],
                        moves=h["moves"],
                        tasks=tasks
                    )
                    hostler_details[h["id"]] = hostler

                # 4. Aggregate result
                result = PollResult(
                    workbasket_tasks=workbasket_tasks,
                    hostlers=hostler_details
                )

                # 5. Store and handle
                await set_latest_poll_result(result)
                await handle_payload(result)
                logger.info("Polling cycle complete.")

            except Exception as e:
                logger.error(f"[Poller] Error: {e}")

            await asyncio.sleep(POLL_INTERVAL)
