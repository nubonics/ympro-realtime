from typing import List, Optional

from fastapi import APIRouter, Depends, Request, HTTPException, Body
from redis.asyncio import Redis

from backend.modules.storage import get_all_tasks
from backend.pega.yard_coordinator.session_manager.manager import PegaTaskSessionManager
from backend.pega.yard_coordinator.deps import PegaTaskPoller
from .colored_logger import setup_logger
from .models import PullTask, BringTask, HookTask, Task, CreateTaskRequest, DeleteTaskRequest, \
    TransferTaskResponse, OpenCase
from backend.pega.yard_coordinator.session_manager.hostler_details import fetch_hostler_details
from backend.pega.yard_coordinator.session_manager.models import ReCreateHostler
from backend.pega.yard_coordinator.transfer.transfer_task import TransferTask
from ..pega.yard_coordinator.toggle_hostler_status.recreate_hostler import ToggleHostlerStatus

router = APIRouter()
logger = setup_logger(__name__)


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


@router.get("/api/external-tasks", response_model=List[Task], tags=["Tasks"])
async def api_get_tasks(
        redis: Redis = Depends(get_redis)
):
    tasks = await get_all_tasks(redis)
    logger.debug(f'external-tasks: {tasks}')
    return [parse_task(t) for t in tasks if t.get("yard_task_type")]


@router.post("/api/create-task", response_model=Task, tags=["Tasks"])
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


# @router.post("/api/transfer-task")
# async def api_transfer_task(
#         request: Request,
#         body: TransferTaskRequest,
#         session_manager: PegaTaskSessionManager = Depends(get_session_manager)
# ):
#     result = await session_manager.run_transfer_task(
#         task_id=body.case_id,
#         assigned_to=body.assigned_to,
#         redis=request.app.state.redis
#     )
#     return {"status": "ok", "result": result}
async def transfer_task_from_hostler(session_manager, base_ref, task_id, assigned_to, redis):
    # --- Step 1: Context extraction (fetch latest task grid, enrich all tasks with context) ---
    hostler_details = await fetch_hostler_details(session_manager, base_ref)
    # hostler_details["tasks"] is a list of dicts with all context fields attached
    logger.debug(f'transfer_task_from_hostler: hostler_details for {base_ref}: {hostler_details}')

    # --- Step 2: Find the task to transfer and perform the transfer ---
    task_to_transfer = next(
        (t for t in hostler_details["tasks"] if t["case_id"] == task_id), None
    )
    if not task_to_transfer:
        raise Exception(f"Task {task_id} not found in hostler grid for {base_ref}")

    # Make sure the task is saved to the store with the latest context
    await session_manager.task_store.upsert_task(task_to_transfer)

    # Run the transfer using the per-task context
    result = await session_manager.run_transfer_task(task_id, assigned_to, redis)

    return result


'''''
@router.post("/api/transfer-task")
async def transfer_task_endpoint(
    request: TransferRequest,
    session_manager=Depends(get_session_manager),
    redis=Depends(get_redis),
):
    result = await session_manager.transfer_task(
        case_id=request.case_id,
        assigned_to=request.assigned_to,
        redis=redis,
    )
    return {"result": result}
'''


@router.post("/api/transfer-task", response_model=TransferTaskResponse, tags=["Tasks"])
async def transfer_task_auto(
        case_id: str = Body(..., embed=True),
        assigned_to: Optional[str] = Body(None, embed=True),
        target: Optional[str] = Body(None, embed=True),
        session_manager: PegaTaskSessionManager = Depends(get_session_manager),
        redis: Redis = Depends(get_redis),
):
    if assigned_to == target:
        raise HTTPException(status_code=400, detail="assigned_to and target must be different")

    task_data = await session_manager.task_store.get_task(case_id)
    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")

    transfer = TransferTask(
        case_id=case_id,
        assigned_to=assigned_to,
        target=target,
        session_manager=session_manager
    )
    result = await transfer.transfer(redis)

    # Defensive: Make sure result is a dict/object matching TransferTaskResponse
    if not result or not isinstance(result, dict):
        raise HTTPException(status_code=500,
                            detail=f"Transfer failed or did not return a valid response. Got: {result}")

    # Optionally, validate required keys
    for k in ["success", "case_id", "assigned_to", "method", "error"]:
        if k not in result:
            raise HTTPException(status_code=500, detail=f"Transfer response missing key: {k}")

    return result


@router.post("/api/delete-task", tags=["Tasks"])
async def api_delete_task(
        body: DeleteTaskRequest,
        session_manager: PegaTaskSessionManager = Depends(get_session_manager)
):
    await session_manager.run_delete_task(body.case_id)
    return {"status": "ok"}


@router.get("/api/hostler-history", tags=["Hostlers"], include_in_schema=False)
async def get_completed_hostler_history(
        session_manager: PegaTaskSessionManager = Depends(get_session_manager)
):
    history = await session_manager.get_completed_hostler_history()
    return {"history": history}


@router.get("/api/refresh-hostler-history", tags=["Hostlers"], include_in_schema=False)
async def refresh_hostler_history(
        session_manager: PegaTaskSessionManager = Depends(get_session_manager)
):
    await session_manager.refresh_all_hostlers_history()
    return {"status": "ok"}


@router.get("/api/poller-status", tags=["Poller"])
async def poller_status(poller: PegaTaskPoller = Depends(get_pega_poller)):
    status = "running" if poller.polling_task and not poller.polling_task.done() else "stopped"
    return {"status": status}


@router.post("/api/poller-stop", tags=["Poller"])
async def stop_poller(poller: PegaTaskPoller = Depends(get_pega_poller)):
    poller.stop_polling()
    return {"stopped": True}


@router.post("/api/poller-start", tags=["Poller"])
async def start_poller(poller: PegaTaskPoller = Depends(get_pega_poller)):
    await poller.start_polling()
    return {"started": True}


@router.post("/api/open-case", tags=["Tasks"])
async def open_case(
        body: OpenCase,
        session_manager: PegaTaskSessionManager = Depends(get_session_manager)
):
    """
    This endpoint is a placeholder for the open case functionality.
    It should be implemented in the PegaTaskSessionManager.
    """
    await session_manager.open_case(case_id=body.case_id, session_manager=session_manager)
    return {"status": "ok", "case_id": body.case_id}


@router.post("/api/re-create-hostler", tags=["Hostlers"])
async def re_create_hostler(
        body: dict = Body(...),
        session_manager: PegaTaskSessionManager = Depends(get_session_manager)
):
    """
    This endpoint re-creates a hostler to put them offline if they forgot to sign out
    The body should contain either 'checker_id' or 'hostler_name' to identify the hostler.
    """
    # Lookup hostler
    hostler_data = None
    if "checker_id" in body:
        hostler_data = await session_manager.hostler_store.get_hostler(body["checker_id"])
    elif "hostler_name" in body:
        checker_id = await session_manager.hostler_store.lookup_checker_id(body["hostler_name"])
        if not checker_id:
            raise HTTPException(status_code=404, detail="Hostler not found by name")
        hostler_data = await session_manager.hostler_store.get_hostler(checker_id)
    else:
        raise HTTPException(status_code=400, detail="checker_id or hostler_name is required")

    if not hostler_data:
        raise HTTPException(status_code=404, detail="Hostler not found")

    # Ensure we have a valid hostler object
    try:
        hostler = ReCreateHostler.model_validate(hostler_data)
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid hostler data")

    # Run the toggle workflow
    toggle_workflow = ToggleHostlerStatus(session_manager, hostler)
    await toggle_workflow.run()

    return {"status": "ok", "checker_id": hostler.checker_id, "name": hostler.name}
