from backend.modules.colored_logger import setup_logger
from pydantic import TypeAdapter

from backend.modules.models import Task
from backend.rules.custom_checks import check_duplicate_task, check_boxtrucks, check_preventative_maintenance

import re

from backend.rules.helper import get_attr

ALLOWED_TYPES = {"pull", "bring", "hook"}
logger = setup_logger(__name__)
TaskAdapter = TypeAdapter(Task)


def passes_business_rules(task, all_tasks):
    """Apply all business rules to a Task instance."""
    # Duplicate check
    allowed, reason = check_duplicate_task(task, all_tasks)
    if not allowed:
        return False, reason
    # Box truck check - ONLY restrict boxtrucks for pull tasks
    trailer_number = get_attr(task, "trailer", "")
    if get_attr(task, "yard_task_type", None) == "pull" and check_boxtrucks(trailer_number):
        return False, f"Box trucks (trailer: {trailer_number}) are not allowed for pull tasks."
    # Preventative maintenance check
    yard_task_type = get_attr(task, "yard_task_type", "")
    if check_preventative_maintenance(yard_task_type=yard_task_type):
        return False, f"Trailer {trailer_number} is flagged for preventative maintenance."

    # Only one active pull or bring per trailer number
    if yard_task_type in ("pull", "bring") and trailer_number:
        for other in all_tasks:
            if (
                other is not task
                and get_attr(other, "yard_task_type") == yard_task_type
                and get_attr(other, "trailer") == trailer_number
            ):
                return False, f"Duplicate {yard_task_type} for trailer {trailer_number} is not allowed."
    return True, None


def get_case_id_numeric(task):
    cid = get_attr(task, "case_id") or get_attr(task, "id") or ""
    if isinstance(cid, str) and cid.startswith("T-"):
        try:
            return int(cid[2:])
        except Exception:
            pass
    try:
        return int(cid)
    except Exception:
        return float('inf')


def dedupe_sort_key(task, use_case_id=False):
    """Return a key for sorting: created_at if allowed, otherwise case id number."""
    if not use_case_id:
        created = get_attr(task, "created_at")
        if created is not None:
            return created
    return get_case_id_numeric(task)


def deduplicate_tasks(task_dicts):
    """
    Deduplicate tasks: keep only the oldest by (type, door).
    If any task in a group is missing created_at, use case id for all.
    """
    grouped = {}
    for task in task_dicts:
        typ = get_attr(task, "type") or get_attr(task, "yard_task_type")
        door = str(get_attr(task, "door")) if get_attr(task, "door") is not None else None
        key = (typ, door)
        grouped.setdefault(key, []).append(task)

    deduped = []
    for key, group in grouped.items():
        # If any task in the group is missing created_at, use case id numeric for all
        use_case_id = any(get_attr(t, "created_at") is None for t in group)
        oldest = min(group, key=lambda t: dedupe_sort_key(t, use_case_id=use_case_id))
        deduped.append(oldest)
    # Add tasks without a door (if you want to keep them all, they are already grouped separately)
    return deduped


def is_allowed_type(task_dict):
    """Check if the task type is allowed."""
    task_type = get_attr(task_dict, "type") or get_attr(task_dict, "yard_task_type")
    return task_type in ALLOWED_TYPES


async def delete_task_external(task_id, task_store, session_manager=None):
    """Delete a task from the external system or just the local store."""
    if session_manager is not None:
        await session_manager.run_delete_task(task_id)
        if await task_store.get_task(task_id) is not None:
            await task_store.delete_task(task_id)
    else:
        await task_store.delete_task(task_id)


async def validate_and_store_task(task_dict, task_store, session_manager=None, all_tasks=None):
    """
    Validate and store a single task. If not valid, delete externally (if possible).
    Returns stored Task or None.
    """
    if not is_allowed_type(task_dict):
        logger.info(
            f"Deleting unwanted yard task type: {get_attr(task_dict, 'type')} for case {get_attr(task_dict, 'case_id') or get_attr(task_dict, 'id')}")
        await delete_task_external(get_attr(task_dict, "id"), task_store, session_manager)
        return None
    try:
        task = TaskAdapter.validate_python(task_dict)
    except Exception as e:
        logger.error(
            f"Could not validate task: {task_dict}, error: {repr(e)}; details: {getattr(e, 'errors', lambda: None)()}")
        await delete_task_external(get_attr(task_dict, "id"), task_store, session_manager)
        return None
    allowed, reason = passes_business_rules(task, all_tasks or [])
    if not allowed:
        logger.info(f"Deleting task {get_attr(task_dict, 'case_id')}: {reason}")
        await delete_task_external(get_attr(task_dict, "case_id") or get_attr(task_dict, "id"), task_store,
                                   session_manager)
        return None
    try:
        await task_store.upsert_task(task.model_dump())
        return task
    except Exception as e:
        logger.error(f"Could not store valid task: {task_dict}, error: {e}")
        return None


async def validate_and_store_tasks(task_dicts, task_store, session_manager=None):
    """
    Deduplicate, validate, and store multiple tasks.
    Delete invalid and deduplicated-out tasks externally if possible.
    Returns only the valid, stored Task instances.
    """
    deduped_task_dicts = deduplicate_tasks(task_dicts)
    deduped_ids = {get_attr(t, "case_id") or get_attr(t, "id") for t in deduped_task_dicts}
    all_ids = {get_attr(t, "case_id") or get_attr(t, "id") for t in task_dicts}
    # Find tasks that were filtered out by deduplication
    removed_ids = all_ids - deduped_ids
    for t in task_dicts:
        tid = get_attr(t, "case_id") or get_attr(t, "id")
        if tid in removed_ids:
            await delete_task_external(tid, task_store, session_manager)
    # Now validate and store deduped tasks
    valid_tasks = []
    for task_dict in deduped_task_dicts:
        task = await validate_and_store_task(
            task_dict, task_store, session_manager=session_manager, all_tasks=valid_tasks
        )
        if task:
            valid_tasks.append(task)
    return valid_tasks
