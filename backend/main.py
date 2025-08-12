import sys
import asyncio

from starlette.middleware.cors import CORSMiddleware

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI

from backend.modules.api_routes import router  # Import only the router, not a new FastAPI app!
from backend.modules.ws_tasks import router as ws_router
from backend.pega.yard_coordinator.session_manager.manager import PegaTaskSessionManager
from redis.asyncio import Redis
from backend.pega.yard_coordinator.deps import PegaTaskPoller

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8052",
        "http://127.0.0.1:8052",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register your API routes
app.include_router(router)
app.include_router(ws_router)


@app.on_event("startup")
async def startup_event():
    redis = await Redis.from_url("redis://localhost", decode_responses=True, db=1)
    await redis.flushdb()
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
