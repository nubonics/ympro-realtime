import redis.asyncio as redis
import json

from backend.pega.yard_coordinator.utils import DateTimeEncoder


class HostlerStore:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def upsert_hostler(self, hostler_data: dict):
        if not hostler_data or not isinstance(hostler_data, dict):
            raise ValueError("Attempted to upsert a hostler with None or non-dict data")
        if "checker_id" not in hostler_data or hostler_data["checker_id"] is None:
            raise ValueError("Hostler data must include a non-None 'checker_id'")
        if "name" not in hostler_data or not isinstance(hostler_data["name"], str):
            raise ValueError("Hostler data must include a non-empty 'name' string")
        key = f"hostler:{hostler_data['checker_id']}"
        await self.redis.set(key, json.dumps(hostler_data, cls=DateTimeEncoder))
        name_key = f"hostler:name:{hostler_data['name'].lower()}"
        await self.redis.set(name_key, hostler_data['checker_id'])

    async def lookup_checker_id(self, assigned_name: str) -> str:
        key = f"hostler:name:{assigned_name.lower()}"
        checker_id = await self.redis.get(key)
        if isinstance(checker_id, bytes):
            return checker_id.decode()
        elif isinstance(checker_id, str):
            return checker_id
        else:
            return ""

    async def get_hostler(self, checker_id: str) -> dict:
        key = f"hostler:{checker_id}"
        data = await self.redis.get(key)
        if not data:
            return {}
        if isinstance(data, bytes):
            data = data.decode()
        return json.loads(data)

    async def list_hostlers(self) -> list:
        keys = await self.redis.keys("hostler:*")
        hostlers = []
        for key in keys:
            # skip name index keys
            if (isinstance(key, bytes) and b':name:' in key) or (isinstance(key, str) and ':name:' in key):
                continue
            data = await self.redis.get(key)
            if not data:
                continue
            if isinstance(data, bytes):
                data = data.decode()
            hostlers.append(json.loads(data))
        return hostlers