from fastapi import FastAPI, HTTPException, Body, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import ValidationError
from redis.asyncio import Redis

from .models import PullTask, BringTask, HookTask, Task
from .rules.validation import check_task_rules
from .storage import (
    create_task,
    get_task,
    get_all_tasks,
    update_task_hostler,
    delete_task,
)
from .deps import get_redis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def parse_task(task_dict):
    ttype = task_dict.get("type")
    try:
        cleaned = {k: (v if v != "" else None) for k, v in task_dict.items()}
        if ttype == "pull":
            return PullTask(**cleaned)
        elif ttype == "bring":
            return BringTask(**cleaned)
        elif ttype == "hook":
            return HookTask(**cleaned)
        else:
            raise HTTPException(status_code=400, detail="Unknown task type.")
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid task data: {e}")


@app.get("/api/external-tasks", response_model=List[Task])
async def api_get_tasks(redis: Redis = Depends(get_redis)):
    tasks = await get_all_tasks(redis)
    return [parse_task(t) for t in tasks if t.get("type")]


@app.post("/api/create-task")
async def api_create_task(request: Request, redis: Redis = Depends(get_redis)):
    task_dict = await request.json()
    try:
        task = parse_task(task_dict)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    all_tasks = await get_all_tasks(redis)
    allowed, reason = check_task_rules(task, all_tasks)   # <--- ADD THIS BLOCK
    if not allowed:
        raise HTTPException(status_code=400, detail=reason)
    await create_task(task.model_dump(), redis)
    return {"status": "ok"}


@app.post("/api/update-task-hostler")
async def api_update_task_hostler(
        id: str = Body(...),
        hostler: str = Body(...),
        redis: Redis = Depends(get_redis),
):
    success = await update_task_hostler(id, hostler, redis)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "ok"}


@app.post("/api/delete-task")
async def api_delete_task(
        id: str = Body(...),
        redis: Redis = Depends(get_redis),
):
    await delete_task(id, redis)
    return {"status": "ok"}
