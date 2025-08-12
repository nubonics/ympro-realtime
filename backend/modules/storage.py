import time
import json
from typing import Dict, Optional, List
from redis.asyncio.client import Redis

from backend.modules.colored_logger import setup_logger
from backend.modules.models import Task  # Task can be a dict or Pydantic model

TASK_KEY_PREFIX = "task:"
TASKS_SET_KEY = "tasks"
LATEST_POLL_RESULT_KEY = "poll_result:latest"
logger = setup_logger(__name__)


def _to_dict(task) -> dict:
    if hasattr(task, "model_dump"):
        return task.model_dump()
    elif hasattr(task, "dict"):
        return task.dict()
    return dict(task)  # fallback for dict


def _from_json(data) -> dict:
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
    await redis.set(task_key, json.dumps(task_dict), ex=ttl)
    await redis.sadd(TASKS_SET_KEY, task_id)
    await rebuild_tasks_set(redis)
    return task_id


async def cleanup_expired_tasks(redis: Redis):
    task_ids = await redis.smembers(TASKS_SET_KEY)
    removed = []
    for tid in task_ids:
        tid_str = tid.decode() if isinstance(tid, bytes) else tid
        task_key = f"{TASK_KEY_PREFIX}{tid_str}"
        exists = await redis.exists(task_key)
        if not exists:
            await redis.srem(TASKS_SET_KEY, tid_str)
            removed.append(tid_str)
    await rebuild_tasks_set(redis)
    return removed


async def get_task(task_id: str, redis: Redis) -> Optional[Dict]:
    task_key = f"{TASK_KEY_PREFIX}{task_id}"
    data = await redis.get(task_key)
    if not data:
        return None
    model_candidate = _from_json(data)
    # Try to validate with Pydantic if possible
    if hasattr(Task, "model_validate"):
        return Task.model_validate(model_candidate)
    return model_candidate  # fallback if Task is just a dict


async def get_all_tasks(redis: Redis) -> List[Dict]:
    task_ids = await redis.smembers(TASKS_SET_KEY)
    # logger.debug(f"Found {len(task_ids)} tasks in Redis")
    # logger.debug(f'Task IDs: {task_ids}')

    tasks = []
    for tid in task_ids:
        tid_str = tid.decode() if isinstance(tid, bytes) else tid
        task = await get_task(tid_str, redis)
        if task:
            tasks.append(task)
    return tasks


async def rebuild_tasks_set(redis: Redis):
    """
    Scan all 'task:*' keys and add their IDs to the 'tasks' set.
    """
    cursor = 0
    task_ids = []
    while True:
        cursor, keys = await redis.scan(cursor=cursor, match=f"{TASK_KEY_PREFIX}*")
        for key in keys:
            key_str = key.decode() if isinstance(key, bytes) else key
            if key_str.startswith(TASK_KEY_PREFIX):
                task_id = key_str[len(TASK_KEY_PREFIX):]
                task_ids.append(task_id)
        if cursor == 0:
            break
    if task_ids:
        await redis.sadd(TASKS_SET_KEY, *task_ids)
        # print(f"Added {len(task_ids)} task IDs to set '{TASKS_SET_KEY}'")
    # else:
    # print("No task keys found to add to set.")


async def update_task_hostler(task_id: str, hostler: Optional[str], redis: Redis) -> bool:
    task_key = f"{TASK_KEY_PREFIX}{task_id}"
    data = await redis.get(task_key)
    if not data:
        return False
    task = _from_json(data)
    task["hostler"] = hostler
    await redis.set(task_key, json.dumps(task))
    await rebuild_tasks_set(redis)
    return True


async def delete_task(task_id: str, redis: Redis):
    task_key = f"{TASK_KEY_PREFIX}{task_id}"
    await redis.delete(task_key)
    await redis.srem(TASKS_SET_KEY, task_id)
    await rebuild_tasks_set(redis)


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
    for task_dict in task_dicts:
        await create_task(task_dict, redis, ttl=ttl)
    await rebuild_tasks_set(redis)


async def get_checker_id_by_name(redis: Redis, name: str) -> str:
    data = await redis.get(f"hostler:name:{name}")
    if isinstance(data, bytes):
        return data.decode()
    return data or ""
