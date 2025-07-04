from os import getenv

from redis.asyncio import Redis

REDIS_URL = getenv("REDIS_URL", "redis://localhost:6379/0")


async def get_redis():
    redis = Redis.from_url(REDIS_URL, decode_responses=True)
    try:
        yield redis
    finally:
        await redis.close()
