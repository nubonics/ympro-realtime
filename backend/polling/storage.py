import aioredis
import json

from backend.polling.models import PollResult

REDIS_URL = "redis://localhost"
TASKS_KEY = "tasks"
PUBSUB_CHANNEL = "frontend_tasks_channel"


async def get_redis():
    """
    Returns a connected Redis client.
    """
    return await aioredis.from_url(REDIS_URL, decode_responses=True)


async def store_task(redis, task):
    """
    Store a validated task in Redis as a JSON string.
    """
    await redis.rpush(TASKS_KEY, json.dumps(task))


async def remove_task(redis, task):
    """
    Remove a task from the Redis tasks list, if present.
    Uses lrem to remove the first occurrence of the serialized task.
    """
    await redis.lrem(TASKS_KEY, 1, json.dumps(task))


async def emit_to_frontend(redis, task):
    """
    Publish a validated task to the pubsub channel for real-time frontend updates.
    """
    await redis.publish(PUBSUB_CHANNEL, json.dumps(task))


async def get_all_tasks(redis):
    """
    Retrieve all tasks from Redis, deserialized from JSON.
    """
    tasks_data = await redis.lrange(TASKS_KEY, 0, -1)
    return [json.loads(t) for t in tasks_data]


async def set_latest_poll_result(result: PollResult):
    redis = await get_redis()
    await redis.set("latest_poll_result", result.json())
    await redis.close()


async def get_latest_poll_result():
    redis = await get_redis()
    data = await redis.get("latest_poll_result")
    await redis.close()
    if data:
        return PollResult.parse_raw(data)
    else:
        return None
