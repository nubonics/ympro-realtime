from os import getenv

import aioredis
from fastapi import FastAPI


def setup_redis_pool(app: FastAPI):
    @app.on_event("startup")
    async def startup():
        REDIS_URL = getenv("REDIS_URL", "redis://localhost")
        app.state.redis = await aioredis.from_url(
            REDIS_URL,
            decode_responses=True,
            max_connections=10,  # adjust as needed
        )

    @app.on_event("shutdown")
    async def shutdown():
        redis = app.state.redis
        if redis:
            await redis.close()
