# backend/main.py
import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from backend.modules.api_routes import app
from backend.pega.yard_coordinator.session_manager.manager import PegaTaskSessionManager
from redis.asyncio import Redis
from backend.pega.yard_coordinator.deps import PegaTaskPoller


@app.on_event("startup")
async def startup_event():
    redis = await Redis.from_url("redis://localhost", decode_responses=True)
    session_manager = PegaTaskSessionManager(redis)
    await session_manager.login()
    await session_manager.deleter.start()
    app.state.session_manager = session_manager
    app.state.redis = redis
    app.state.pega_poller = PegaTaskPoller(session_manager, redis)
