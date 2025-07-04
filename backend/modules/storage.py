import uuid
import json
from typing import Dict, Optional, List
from redis.asyncio.client import Redis

from backend.modules.models import Task

TASKS_KEY = "tasks"
LATEST_POLL_RESULT_KEY = "poll_result:latest"


def _to_dict(task: Task) -> dict:
    # Use model_dump if available (Pydantic v2+), else .dict()
    if hasattr(task, "model_dump"):
        return task.model_dump()
    return task.dict()


def _from_json(data) -> dict:
    # Redis might return bytes, decode if needed
    if isinstance(data, bytes):
        data = data.decode()
    return json.loads(data)


async def create_task(task_dict: Dict, redis: Redis) -> str:
    """
    Create or replace a task in the Redis list by id.
    """
    task_id = task_dict.get("id") or str(uuid.uuid4())
    task_dict["id"] = task_id
    await delete_task(task_id, redis)  # Remove any existing task with same id to prevent duplicates
    await redis.rpush(TASKS_KEY, json.dumps(task_dict))
    return task_id


async def get_task(task_id: str, redis: Redis) -> Optional[Task]:
    """
    Retrieve a task by id.
    """
    tasks_data = await redis.lrange(TASKS_KEY, 0, -1)
    for t in tasks_data:
        task = _from_json(t)
        if task.get("id") == task_id:
            # return Task(**task)
            return [Task.model_validate(task)]
    return None


async def get_all_tasks(redis: Redis) -> List[Task]:
    """
    Return all tasks as Task objects.
    """
    tasks_data = await redis.lrange(TASKS_KEY, 0, -1)
    # return [Task(**_from_json(t)) for t in tasks_data]
    return [Task.model_validate(_from_json(t)) for t in tasks_data]


async def update_task_hostler(task_id: str, hostler: Optional[str], redis: Redis) -> bool:
    """
    Update the 'hostler' field of a specific task.
    """
    tasks_data = await redis.lrange(TASKS_KEY, 0, -1)
    for idx, t in enumerate(tasks_data):
        task = _from_json(t)
        if task.get("id") == task_id:
            task["hostler"] = hostler
            await redis.lset(TASKS_KEY, idx, json.dumps(task))
            return True
    return False


async def delete_task(task_id: str, redis: Redis):
    """
    Remove a task by id.
    """
    tasks_data = await redis.lrange(TASKS_KEY, 0, -1)
    for t in tasks_data:
        task = _from_json(t)
        if task.get("id") == task_id:
            await redis.lrem(TASKS_KEY, 1, t)
            break


async def set_latest_poll_result(poll_result: dict, redis: Redis):
    """
    Save the latest poll result as a JSON string.
    """
    await redis.set(LATEST_POLL_RESULT_KEY, json.dumps(poll_result))


async def get_latest_poll_result(redis: Redis) -> Optional[dict]:
    """
    Get the latest poll result as a dict, or None if not set.
    """
    data = await redis.get(LATEST_POLL_RESULT_KEY)
    if data is None:
        return None
    if isinstance(data, bytes):
        data = data.decode()
    return json.loads(data)


# Note: Task validation/fixing should happen before calling import_tasks.
async def import_tasks(task_dicts: List[Dict], redis: Redis):
    """
    Import a list of task dicts, overwriting existing tasks with the same ids.
    """
    for task_dict in task_dicts:
        await create_task(task_dict, redis)
