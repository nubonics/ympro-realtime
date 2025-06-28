from fastapi import FastAPI, Depends, HTTPException, Body
from .redis_pool import setup_redis_pool
from .dependencies import get_redis
from .redis_tasks import (
    create_task,
    get_task,
    get_all_tasks,
    update_task_hostler,
    delete_task,
)

app = FastAPI()
setup_redis_pool(app)


@app.post("/tasks")
async def api_create_task(task: dict, redis=Depends(get_redis)):
    task_id = await create_task(task, redis)
    return {"task_id": task_id}


@app.get("/tasks/{task_id}")
async def api_get_task(task_id: str, redis=Depends(get_redis)):
    task = await get_task(task_id, redis)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/tasks")
async def api_get_all_tasks(redis=Depends(get_redis)):
    return await get_all_tasks(redis)


@app.post("/tasks/{task_id}/hostler")
async def api_update_task_hostler(task_id: str, hostler: str = Body(...), redis=Depends(get_redis)):
    success = await update_task_hostler(task_id, hostler, redis)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "ok"}


@app.delete("/tasks/{task_id}")
async def api_delete_task(task_id: str, redis=Depends(get_redis)):
    await delete_task(task_id, redis)
    return {"status": "deleted"}
