import asyncio
import random
import uuid
from redis.asyncio import Redis
import json

TASKS_KEY = "tasks"
DEFAULT_REDIS_URL = "redis://127.0.0.1:6379/1"

PULL_TEMPLATE = {
    "type": "pull",
    "door": "A{}",
    "trailer": "TR-{}",
    "zoneType": "dock",
    "zoneLocation": "Z{}",
    "note": "Fake pull task {}",
    "priority": "normal",
    "hostler": None
}
BRING_TEMPLATE = {
    "type": "bring",
    "door": "B{}",
    "trailer": "TR-{}",
    "zoneType": "yard",
    "zoneLocation": "Y{}",
    "note": "Fake bring task {}",
    "priority": "normal",
    "hostler": None
}
HOOK_TEMPLATE = {
    "type": "hook",
    "leadTrailer": "TR-{}",
    "leadDoor": "C{}",
    "middleTrailer": "TR-MID-{}",
    "middleDoor": "D{}",
    "dolly1": None,
    "tailTrailer": "TR-TAIL-{}",
    "tailDoor": None,
    "dolly2": None,
    "note": "Fake hook task {}",
    "priority": "normal",
    "hostler": None
}


def make_task(template, idx):
    task = template.copy()
    task["id"] = str(uuid.uuid4())
    for key in task:
        if isinstance(task[key], str):
            task[key] = task[key].format(idx)
    return task


async def add_fake_tasks(num_tasks=10, redis_url=DEFAULT_REDIS_URL):
    redis = Redis.from_url(redis_url, decode_responses=True)
    task_types = ["pull", "bring", "hook"]
    templates = {
        "pull": PULL_TEMPLATE,
        "bring": BRING_TEMPLATE,
        "hook": HOOK_TEMPLATE,
    }
    for i in range(num_tasks):
        task_type = random.choice(task_types)
        task = make_task(templates[task_type], i + 1)
        await redis.rpush(TASKS_KEY, json.dumps(task))
        print(f"Added fake {task_type} task: {task['id']}")
    await redis.aclose()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Add fake tasks to Redis for testing.")
    parser.add_argument("--num", type=int, default=5, help="Number of fake tasks to add")
    parser.add_argument("--redis-url", type=str, default=DEFAULT_REDIS_URL, help="Redis URL")
    args = parser.parse_args()

    asyncio.run(add_fake_tasks(args.num, args.redis_url))
