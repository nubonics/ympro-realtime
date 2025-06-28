from .api import app

# Optionally, if you want to add custom startup/shutdown events, you can do so here:
# from deps import get_redis
# @app.on_event("startup")
# async def startup():
#     # e.g., warm up cache or test Redis connection
#     redis = await anext(get_redis())
#     await redis.ping()

# The app is imported from api.py and ready for uvicorn or Gunicorn.
# uvicorn backend.main:app --reload
