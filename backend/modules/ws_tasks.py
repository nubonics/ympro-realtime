# backend/ws_tasks.py
from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect
from backend.modules.tasks_hub import tasks_hub

router = APIRouter()


@router.websocket("/ws/tasks")
async def ws_tasks(ws: WebSocket):
    await tasks_hub.register(ws)
    try:
        while True:
            # no client messages required; keeps the connection alive
            await ws.receive_text()
    except WebSocketDisconnect:
        await tasks_hub.unregister(ws)
    except Exception:
        await tasks_hub.unregister(ws)
