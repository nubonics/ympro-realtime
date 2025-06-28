import redis.asyncio as redis
import json


class TaskStore:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def upsert_task(self, task_data: dict):
        key = f"task:{task_data['id']}"
        await self.redis.set(key, json.dumps(task_data))

    async def get_task(self, task_id: str) -> dict:
        key = f"task:{task_id}"
        data = await self.redis.get(key)
        return json.loads(data) if data else {}

    async def list_tasks(self) -> list:
        keys = await self.redis.keys("task:*")
        tasks = []
        for key in keys:
            data = await self.redis.get(key)
            if data:
                tasks.append(json.loads(data))
        return tasks

    async def delete_task(self, task_id: str):
        key = f"task:{task_id}"
        await self.redis.delete(key)
