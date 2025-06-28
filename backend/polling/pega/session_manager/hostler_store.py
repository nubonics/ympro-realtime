import redis.asyncio as redis
import json


class HostlerStore:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def upsert_hostler(self, hostler_data: dict):
        key = f"hostler:{hostler_data['checker_id']}"
        await self.redis.set(key, json.dumps(hostler_data))
        name_key = f"hostler:name:{hostler_data['name'].lower()}"
        await self.redis.set(name_key, hostler_data['checker_id'])

    async def lookup_checker_id(self, assigned_name: str) -> str:
        key = f"hostler:name:{assigned_name.lower()}"
        checker_id = await self.redis.get(key)
        return checker_id.decode() if checker_id else ""

    async def get_hostler(self, checker_id: str) -> dict:
        key = f"hostler:{checker_id}"
        data = await self.redis.get(key)
        return json.loads(data) if data else {}

    async def list_hostlers(self) -> list:
        keys = await self.redis.keys("hostler:*")
        hostlers = []
        for key in keys:
            if b':name:' in key:
                continue
            data = await self.redis.get(key)
            if data:
                hostlers.append(json.loads(data))
        return hostlers
