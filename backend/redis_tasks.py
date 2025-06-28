import redis
import uuid

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
TASK_SET = "task_ids"


def create_task(task_dict):
    task_id = task_dict.get("id") or str(uuid.uuid4())
    task_dict["id"] = task_id
    redis_dict = {k: str(v) if v is not None else "" for k, v in task_dict.items()}
    r.hset(f"task:{task_id}", mapping=redis_dict)
    r.sadd(TASK_SET, task_id)
    return task_id


def get_task(task_id):
    data = r.hgetall(f"task:{task_id}")
    return data if data else None


def get_all_tasks():
    ids = r.smembers(TASK_SET)
    return [r.hgetall(f"task:{id}") for id in ids]


def update_task_hostler(task_id, hostler):
    if r.exists(f"task:{task_id}"):
        r.hset(f"task:{task_id}", "hostler", hostler or "")
        return True
    return False


def delete_task(task_id):
    r.delete(f"task:{task_id}")
    r.srem(TASK_SET, task_id)
