from fastapi import FastAPI, HTTPException, Depends
import asyncio
from .poller import poll_forever, set_latest_poll_result
from .models import PollResult
from ..storage import get_latest_poll_result
from ..deps import get_redis
from redis.asyncio import Redis

app = FastAPI()


# Handle new poll results (store latest in Redis)
async def handle_payload(payload: PollResult, redis: Redis):
    await set_latest_poll_result(payload.model_dump(), redis)


@app.on_event("startup")
async def start_poller():
    # Dependency injection not directly available here, so create redis manually
    from ..deps import REDIS_URL
    redis = Redis.from_url(REDIS_URL, decode_responses=True)

    async def handler(payload):
        await set_latest_poll_result(payload.model_dump(), redis)

    asyncio.create_task(poll_forever(handler))


@app.get("/latest-poll", response_model=PollResult)
async def get_latest_poll(redis: Redis = Depends(get_redis)):
    """
    Returns the most recent polling data.
    """
    data = await get_latest_poll_result(redis)
    if not data:
        raise HTTPException(status_code=404, detail="No poll result available")
    return PollResult(**data)
