import uuid
import json
from typing import Dict, Optional, List
from redis.asyncio.client import Redis

from backend.models import Task
from backend.rules.validation import validate_and_fix_tasks

TASKS_KEY = "tasks"
LATEST_POLL_RESULT_KEY = "poll_result:latest"


async def create_task(task_dict: Dict, redis: Redis) -> str:
    task_id = task_dict.get("id") or str(uuid.uuid4())
    task_dict["id"] = task_id
    await redis.rpush(TASKS_KEY, json.dumps(task_dict))
    return task_id


async def get_task(task_id: str, redis: Redis) -> Optional[Dict]:
    tasks_data = await redis.lrange(TASKS_KEY, 0, -1)
    for t in tasks_data:
        task = json.loads(t)
        if task.get("id") == task_id:
            return task
    return None


async def get_all_tasks(redis: Redis) -> List[Dict]:
    tasks_data = await redis.lrange(TASKS_KEY, 0, -1)
    return [json.loads(t) for t in tasks_data]


async def update_task_hostler(task_id: str, hostler: Optional[str], redis: Redis) -> bool:
    tasks_data = await redis.lrange(TASKS_KEY, 0, -1)
    for idx, t in enumerate(tasks_data):
        task = json.loads(t)
        if task.get("id") == task_id:
            task["hostler"] = hostler
            await redis.lset(TASKS_KEY, idx, json.dumps(task))
            return True
    return False


async def delete_task(task_id: str, redis: Redis):
    tasks_data = await redis.lrange(TASKS_KEY, 0, -1)
    for t in tasks_data:
        task = json.loads(t)
        if task.get("id") == task_id:
            await redis.lrem(TASKS_KEY, 1, t)
            break


async def set_latest_poll_result(poll_result: dict, redis: Redis):
    """Save the latest poll result as a JSON string."""
    await redis.set(LATEST_POLL_RESULT_KEY, json.dumps(poll_result))


async def get_latest_poll_result(redis: Redis) -> Optional[dict]:
    """Get the latest poll result as a dict, or None if not set."""
    data = await redis.get(LATEST_POLL_RESULT_KEY)
    if data is None:
        return None
    return json.loads(data)


async def import_tasks(task_dicts, redis):
    # Convert dicts to Task objects
    tasks = [Task(**td) for td in task_dicts]
    fixed_tasks = validate_and_fix_tasks(tasks)
    # Store each fixed task in Redis
    for task in fixed_tasks:
        await create_task(task.dict(), redis)
