from typing import List

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis

from backend.modules.storage import get_all_tasks
from backend.pega.yard_coordinator.session_manager.manager import PegaTaskSessionManager
from backend.pega.yard_coordinator.deps import PegaTaskPoller
from .models import PullTask, BringTask, HookTask, Task, CreateTaskRequest, TransferTaskRequest, DeleteTaskRequest

router = APIRouter()


# CORS middleware should be set on the main app, not on the router!

# --- Dependency helpers ---

def get_session_manager(request: Request) -> PegaTaskSessionManager:
    return request.app.state.session_manager


def get_pega_poller(request: Request) -> PegaTaskPoller:
    return request.app.state.pega_poller


def get_redis(request: Request) -> Redis:
    return request.app.state.redis


# --- API ROUTES ---

def parse_task(task_dict):
    if task_dict is None:
        raise HTTPException(status_code=500, detail="parse_task received None instead of a task dict")
    ttype = task_dict.get("yard_task_type")
    try:
        cleaned = {k: (v if v != "" else None) for k, v in task_dict.items()}
        if ttype == "pull":
            return PullTask.model_validate(cleaned)
        elif ttype == "bring":
            return BringTask.model_validate(cleaned)
        elif ttype == "hook":
            return HookTask.model_validate(cleaned)
        else:
            raise HTTPException(status_code=400, detail="Unknown yard_task_type.")
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid task data: {e}")


@router.get("/api/external-tasks", response_model=List[Task])
async def api_get_tasks(
        redis: Redis = Depends(get_redis)
):
    tasks = await get_all_tasks(redis)
    return [parse_task(t) for t in tasks if t.get("yard_task_type")]


@router.post("/api/create-task", response_model=Task)
async def api_create_task(
        body: CreateTaskRequest,
        session_manager: PegaTaskSessionManager = Depends(get_session_manager)
):
    task_dict = body.dict()
    created_task_data = await session_manager.run_create_task(
        yard_task_type=task_dict["yard_task_type"],
        trailer_number=task_dict.get("trailer"),
        door=task_dict.get("door"),
        assigned_to=task_dict.get("assigned_to"),
        status=task_dict.get("status", "PENDING"),
        locked=task_dict.get("locked", False),
        general_note=task_dict.get("general_note", ""),
        priority=task_dict.get("priority", "Normal"),
    )
    try:
        task = parse_task(created_task_data)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    return task


@router.post("/api/transfer-task")
async def api_transfer_task(
        request: Request,
        body: TransferTaskRequest,
        session_manager: PegaTaskSessionManager = Depends(get_session_manager)
):
    result = await session_manager.run_transfer_task(
        task_id=body.case_id,
        assigned_to=body.assigned_to,
        redis=request.app.state.redis
    )
    return {"status": "ok", "result": result}


@router.post("/api/delete-task")
async def api_delete_task(
        body: DeleteTaskRequest,
        session_manager: PegaTaskSessionManager = Depends(get_session_manager)
):
    await session_manager.run_delete_task(body.case_id)
    return {"status": "ok"}


@router.get("/api/hostler-history")
async def get_completed_hostler_history(
        session_manager: PegaTaskSessionManager = Depends(get_session_manager)
):
    history = await session_manager.get_completed_hostler_history()
    return {"history": history}


@router.post("/api/refresh-hostler-history")
async def refresh_hostler_history(
        session_manager: PegaTaskSessionManager = Depends(get_session_manager)
):
    await session_manager.refresh_all_hostlers_history()
    return {"status": "ok"}


@router.get("/api/poller-status")
async def poller_status(poller: PegaTaskPoller = Depends(get_pega_poller)):
    status = "running" if poller.polling_task and not poller.polling_task.done() else "stopped"
    return {"status": status}


@router.post("/api/poller-stop")
async def stop_poller(poller: PegaTaskPoller = Depends(get_pega_poller)):
    poller.stop_polling()
    return {"stopped": True}


@router.post("/api/poller-start")
async def start_poller(poller: PegaTaskPoller = Depends(get_pega_poller)):
    await poller.start_polling()
    return {"started": True}
