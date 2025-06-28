import os
import httpx
import asyncio

POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "10"))  # seconds
BASE_URL = os.getenv("POLLER_URL", "http://localhost:8001")


async def fetch_workbasket(client):
    resp = await client.get(f"{BASE_URL}/workbasket")
    resp.raise_for_status()
    return resp.json()["tasks"]


async def fetch_hostlers_summary(client):
    resp = await client.get(f"{BASE_URL}/hostlers/summary")
    resp.raise_for_status()
    return resp.json()["hostlers"]


async def fetch_hostler_details(client, hostler_id):
    resp = await client.get(f"{BASE_URL}/hostlers/{hostler_id}/details")
    resp.raise_for_status()
    return resp.json()["tasks"]


async def poll_forever(handle_payload):
    async with httpx.AsyncClient() as client:
        while True:
            try:
                # 1. Fetch unassigned tasks
                workbasket_tasks = await fetch_workbasket(client)

                # 2. Fetch hostler summary
                hostlers = await fetch_hostlers_summary(client)

                # 3. For each hostler, fetch assigned tasks
                hostler_details = {}
                for hostler in hostlers:
                    tasks = await fetch_hostler_details(client, hostler["id"])
                    hostler_details[hostler["id"]] = {
                        "name": hostler["name"],
                        "checker_id": hostler["checker_id"],
                        "moves": hostler["moves"],
                        "tasks": tasks
                    }

                # 4. Call the handler with the full polling result
                await handle_payload({
                    "workbasket_tasks": workbasket_tasks,
                    "hostlers": hostler_details
                })

            except Exception as e:
                print(f"[Poller] Error: {e}")

            await asyncio.sleep(POLL_INTERVAL)
