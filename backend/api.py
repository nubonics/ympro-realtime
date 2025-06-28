from fastapi import FastAPI, HTTPException, Body, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import ValidationError

from models import PullTask, BringTask, HookTask, Task
from redis_tasks import create_task, get_task, get_all_tasks, update_task_hostler, delete_task
from pubsub import publish_event, r as redis_pub, TASK_CHANNEL

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
def api_get_tasks():
    tasks = get_all_tasks()
    return [parse_task(t) for t in tasks if t.get("type")]


@app.post("/api/create-task")
async def api_create_task(request: Request):
    task_dict = await request.json()
    try:
        task = parse_task(task_dict)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    create_task(task.model_dump())
    publish_event("created", task.model_dump())
    return {"status": "ok"}


@app.post("/api/update-task-hostler")
def api_update_task_hostler(id: str = Body(...), hostler: str = Body(...)):
    success = update_task_hostler(id, hostler)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    task = get_task(id)
    if task:
        publish_event("updated", task)
    return {"status": "ok"}


@app.post("/api/delete-task")
def api_delete_task(id: str = Body(...)):
    task = get_task(id)
    delete_task(id)
    if task:
        publish_event("deleted", task)
    return {"status": "ok"}


@app.websocket("/ws/tasks")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    pubsub = redis_pub.pubsub()
    pubsub.subscribe(TASK_CHANNEL)
    try:
        for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_text(message["data"])
    finally:
        pubsub.unsubscribe(TASK_CHANNEL)
        await websocket.close()
