import redis.asyncio as redis
import json
import os

REDIS_PUBSUB_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class PubSubManager:
    def __init__(self, redis_client=None):
        self.redis = redis_client or redis.from_url(REDIS_PUBSUB_URL, decode_responses=True)

    async def publish(self, channel: str, payload: dict):
        message = json.dumps(payload)
        await self.redis.publish(channel, message)
