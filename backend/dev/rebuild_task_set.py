import asyncio
from redis.asyncio import Redis

TASK_KEY_PREFIX = "task:"
TASKS_SET_KEY = "tasks"


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
        print(f"Added {len(task_ids)} task IDs to set '{TASKS_SET_KEY}'")
    else:
        print("No task keys found to add to set.")


async def main():
    redis = Redis(host="localhost", port=6379, db=1)  # adjust host/port/db if needed
    await rebuild_tasks_set(redis)
    await redis.close()


if __name__ == "__main__":
    asyncio.run(main())
