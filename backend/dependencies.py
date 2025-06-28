from fastapi import Request, Depends


async def get_redis(request: Request):
    return request.app.state.redis
