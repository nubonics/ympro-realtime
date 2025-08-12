# backend/tasks_hub.py
import asyncio, json
from typing import Any, Dict, List, Set
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect


class TasksHub:
    def __init__(self):
        self._clients: Set[WebSocket] = set()
        self._lock = asyncio.Lock()
        self._snapshot: List[Dict[str, Any]] = []
        self._keepalive_secs = 25

    async def register(self, ws: WebSocket):
        await ws.accept()
        async with self._lock:
            self._clients.add(ws)
        # send current snapshot immediately
        await self._send_snapshot_to(ws)
        # keepalive
        asyncio.create_task(self._keepalive(ws))

    async def unregister(self, ws: WebSocket):
        async with self._lock:
            self._clients.discard(ws)

    async def _keepalive(self, ws: WebSocket):
        try:
            while True:
                await asyncio.sleep(self._keepalive_secs)
                await ws.send_text('{"type":"ping"}')
        except Exception:
            await self.unregister(ws)

    async def _send_snapshot_to(self, ws: WebSocket):
        await ws.send_text(json.dumps(self._snapshot, default=str))

    async def set_snapshot(self, tasks: List[Dict[str, Any]]):
        """Set the latest snapshot and broadcast to all clients."""
        self._snapshot = tasks or []
        payload = json.dumps(self._snapshot, default=str)
        async with self._lock:
            clients = list(self._clients)
        for client in clients:
            try:
                await client.send_text(payload)
            except Exception:
                await self.unregister(client)


tasks_hub = TasksHub()
