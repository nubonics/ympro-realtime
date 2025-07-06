import redis.asyncio as redis
import json
import os

from backend.pega.yard_coordinator.utils import DateTimeEncoder

REDIS_PUBSUB_URL = os.getenv("REDIS_URL", "redis://localhost:6379/1")


class PubSubManager:
    def __init__(self, redis_client=None):
        self.redis = redis_client or redis.from_url(REDIS_PUBSUB_URL, decode_responses=True)

    async def publish(self, channel: str, payload: str):
        message = json.dumps(payload, cls=DateTimeEncoder)
        await self.redis.publish(channel, message)
