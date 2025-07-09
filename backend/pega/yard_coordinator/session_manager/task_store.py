import redis.asyncio as redis
import json

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
        safe_data = json.dumps(task_data, cls=DateTimeEncoder)
        await self.redis.set(key, safe_data)

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

    async def list_tasks(self) -> list:
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

    # --- Hostler methods below ---
    async def upsert_hostler(self, hostler_data: dict):
        if not hostler_data or not isinstance(hostler_data, dict):
            raise ValueError("Attempted to upsert hostler with None or non-dict data")
        if "checker_id" not in hostler_data or hostler_data["checker_id"] is None:
            raise ValueError("Hostler data must include a non-None 'checker_id'")
        key = f"hostler:{hostler_data['checker_id']}"
        safe_data = json.dumps(hostler_data, cls=DateTimeEncoder)
        await self.redis.set(key, safe_data)

    async def get_hostler(self, checker_id: str) -> dict:
        key = f"hostler:{checker_id}"
        data = await self.redis.get(key)
        return json.loads(data) if data else {}
