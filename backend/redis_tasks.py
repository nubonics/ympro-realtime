import uuid
from typing import Dict, Optional, List

TASK_SET = "task_ids"


async def create_task(task_dict: Dict, redis) -> str:
    task_id = task_dict.get("id") or str(uuid.uuid4())
    task_dict["id"] = task_id
    redis_dict = {k: str(v) if v is not None else "" for k, v in task_dict.items()}
    await redis.hset(f"task:{task_id}", mapping=redis_dict)
    await redis.sadd(TASK_SET, task_id)
    return task_id


async def get_task(task_id: str, redis) -> Optional[Dict]:
    data = await redis.hgetall(f"task:{task_id}")
    return data if data else None


async def get_all_tasks(redis) -> List[Dict]:
    ids = await redis.smembers(TASK_SET)
    tasks = []
    for id in ids:
        task = await redis.hgetall(f"task:{id}")
        if task:
            tasks.append(task)
    return tasks


async def update_task_hostler(task_id: str, hostler: Optional[str], redis) -> bool:
    exists = await redis.exists(f"task:{task_id}")
    if exists:
        await redis.hset(f"task:{task_id}", "hostler", hostler or "")
        return True
    return False


async def delete_task(task_id: str, redis):
    await redis.delete(f"task:{task_id}")
    await redis.srem(TASK_SET, task_id)
