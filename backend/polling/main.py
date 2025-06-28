from fastapi import FastAPI
import asyncio
from .poller import poll_forever
from .store import poller_store
from .models import PollResult

app = FastAPI()

# Handle new poll results (replace with your own upsert/broadcast logic)
async def handle_payload(payload: PollResult):
    # For demonstration, do nothing (already stored in poller_store).
    pass

@app.on_event("startup")
async def start_poller():
    asyncio.create_task(poll_forever(handle_payload))

@app.get("/latest-poll", response_model=PollResult)
async def get_latest_poll():
    """
    Returns the most recent polling data.
    """
    data = poller_store.get_latest()
    if data is None:
        return {}  # or raise 404
    return data