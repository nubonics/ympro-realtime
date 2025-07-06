import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI

from backend.modules.api_routes import router  # Import only the router, not a new FastAPI app!
from backend.pega.yard_coordinator.session_manager.manager import PegaTaskSessionManager
from redis.asyncio import Redis
from backend.pega.yard_coordinator.deps import PegaTaskPoller

app = FastAPI()

# Register your API routes
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    redis = await Redis.from_url("redis://localhost", decode_responses=True, db=1)
    session_manager = PegaTaskSessionManager(redis)
    await session_manager.login()
    await session_manager.deleter.start()
    app.state.session_manager = session_manager
    app.state.redis = redis
    app.state.pega_poller = PegaTaskPoller(session_manager, redis)


@app.on_event("shutdown")
async def shutdown_event():
    if hasattr(app.state, "pega_poller"):
        app.state.pega_poller.stop_polling()
    if hasattr(app.state, "session_manager"):
        await app.state.session_manager.deleter.shutdown()
        await app.state.session_manager.close()
    if hasattr(app.state, "redis"):
        await app.state.redis.close()
