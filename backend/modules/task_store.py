import redis.asyncio as redis
import json

from backend.modules.storage import rebuild_tasks_set
from backend.pega.yard_coordinator.utils import DateTimeEncoder


class TaskStore:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def upsert_task(self, task_data: dict):
        if not task_data or not isinstance(task_data, dict):
            raise ValueError("Attempted to upsert a task with None or non-dict data")
        if "case_id" not in task_data or task_data["case_id"] is None:
            raise ValueError("Task data must include a non-None 'case_id'")
        key = f"task:{task_data['case_id']}"
        # Save as pretty-printed JSON for human readability
        safe_data = json.dumps(task_data, cls=DateTimeEncoder, indent=4)
        await self.redis.set(key, safe_data)
        await rebuild_tasks_set(self.redis)

    async def get_task(self, case_id: str) -> dict:
        key = f"task:{case_id}"
        data = await self.redis.get(key)
        return json.loads(data) if data else {}

    async def get_all_tasks(self) -> list:
        keys = await self.redis.keys("task:*")
        tasks = []
        for key in keys:
            data = await self.redis.get(key)
            if data:
                tasks.append(json.loads(data))
        return tasks

    async def delete_task(self, case_id: str):
        key = f"task:{case_id}"
        await self.redis.delete(key)
        await rebuild_tasks_set(self.redis)

    async def clear_all_tasks(self):
        keys = await self.redis.keys("task:*")
        if keys:
            await self.redis.delete(*keys)
        await rebuild_tasks_set(self.redis)
