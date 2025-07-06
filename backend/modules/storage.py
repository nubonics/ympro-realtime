import time
import json
from typing import Dict, Optional, List
from redis.asyncio.client import Redis

from backend.modules.models import Task

TASK_KEY_PREFIX = "task:"
TASKS_SET_KEY = "tasks"
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


async def create_task(task_dict: dict, redis: Redis, ttl: int = 3600) -> str:
    task_id = task_dict.get("case_id")
    if not task_id:
        raise ValueError("Task must have a case_id")
    task_dict["case_id"] = task_id
    task_dict["saved_at"] = int(time.time())
    task_key = f"{TASK_KEY_PREFIX}{task_id}"
    # Store as a separate key with TTL, and track in the set of task IDs
    await redis.set(task_key, json.dumps(task_dict), ex=ttl)
    await redis.sadd(TASKS_SET_KEY, task_id)
    return task_id


async def cleanup_expired_tasks(redis: Redis):
    """
    Remove task IDs from the set whose keys no longer exist (expired).
    """
    task_ids = await redis.smembers(TASKS_SET_KEY)
    removed = []
    for tid in task_ids:
        tid_str = tid.decode() if isinstance(tid, bytes) else tid
        task_key = f"{TASK_KEY_PREFIX}{tid_str}"
        exists = await redis.exists(task_key)
        if not exists:
            await redis.srem(TASKS_SET_KEY, tid_str)
            removed.append(tid_str)
    return removed


async def get_task(task_id: str, redis: Redis) -> Optional[Task]:
    task_key = f"{TASK_KEY_PREFIX}{task_id}"
    data = await redis.get(task_key)
    if not data:
        return None
    return Task.model_validate(_from_json(data))


async def get_all_tasks(redis: Redis) -> List[Task]:
    task_ids = await redis.smembers(TASKS_SET_KEY)
    tasks = []
    for tid in task_ids:
        tid_str = tid.decode() if isinstance(tid, bytes) else tid
        task = await get_task(tid_str, redis)
        if task:
            tasks.append(task)
    return tasks


async def update_task_hostler(task_id: str, hostler: Optional[str], redis: Redis) -> bool:
    task_key = f"{TASK_KEY_PREFIX}{task_id}"
    data = await redis.get(task_key)
    if not data:
        return False
    task = _from_json(data)
    task["hostler"] = hostler
    await redis.set(task_key, json.dumps(task))
    return True


async def delete_task(task_id: str, redis: Redis):
    task_key = f"{TASK_KEY_PREFIX}{task_id}"
    await redis.delete(task_key)
    await redis.srem(TASKS_SET_KEY, task_id)


async def set_latest_poll_result(poll_result: dict, redis: Redis):
    await redis.set(LATEST_POLL_RESULT_KEY, json.dumps(poll_result))


async def get_latest_poll_result(redis: Redis) -> Optional[dict]:
    data = await redis.get(LATEST_POLL_RESULT_KEY)
    if data is None:
        return None
    if isinstance(data, bytes):
        data = data.decode()
    return json.loads(data)


async def import_tasks(task_dicts: List[Dict], redis: Redis, ttl: int = 3600):
    """
    Import a list of task dicts, overwriting existing tasks with the same ids.
    """
    for task_dict in task_dicts:
        await create_task(task_dict, redis, ttl=ttl)


async def get_checker_id_by_name(redis: Redis, name: str) -> str:
    # Example: hostler:name:{name} => checker_id
    return await redis.get(f"hostler:name:{name}")
