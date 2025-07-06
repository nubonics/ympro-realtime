import json
from redis.asyncio.client import Redis

TASK_CHANNEL = "tasks-events"

async def publish_event(event_type: str, task: dict, redis: Redis):
    """
    Publishes a task event to the pubsub channel.
    Usage: await publish_event("created", task_dict, redis)
    """
    data = json.dumps({
        "event": event_type,  # "created", "updated", "deleted"
        "task": task
    })
    await redis.publish(TASK_CHANNEL, data)