import json

TASK_DETAIL_CACHE_KEY = "task_details:{}"


class TaskCache:
    def __init__(self, redis):
        self.redis = redis

    async def get(self, task_id):
        key = TASK_DETAIL_CACHE_KEY.format(task_id)
        cached = await self.redis.get(key)
        return json.loads(cached) if cached else None

    async def set(self, task_id, details):
        key = TASK_DETAIL_CACHE_KEY.format(task_id)
        await self.redis.set(key, json.dumps(details))

    async def delete(self, task_id):
        key = TASK_DETAIL_CACHE_KEY.format(task_id)
        await self.redis.delete(key)
