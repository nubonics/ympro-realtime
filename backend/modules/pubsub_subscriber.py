import redis.asyncio as redis
import asyncio
import json
import os

REDIS_PUBSUB_URL = os.getenv("REDIS_URL", "redis://localhost:6379/1")


async def main():
    redis_client = redis.from_url(REDIS_PUBSUB_URL, decode_responses=True)
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("hostler_update", "workbasket_update")
    async for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            print(f"Received update on {message['channel']}: {data}")


if __name__ == "__main__":
    asyncio.run(main())
