from fastapi import FastAPI, HTTPException
import asyncio
from .poller import poll_forever, set_latest_poll_result
from .models import PollResult
from .storage import get_latest_poll_result

app = FastAPI()


# Handle new poll results (store latest in Redis)
async def handle_payload(payload: PollResult):
    await set_latest_poll_result(payload)


@app.on_event("startup")
async def start_poller():
    asyncio.create_task(poll_forever(handle_payload))


@app.get("/latest-poll", response_model=PollResult)
async def get_latest_poll():
    """
    Returns the most recent polling data.
    """
    data = await get_latest_poll_result()
    if not data:
        raise HTTPException(status_code=404, detail="No poll result available")
    return data
