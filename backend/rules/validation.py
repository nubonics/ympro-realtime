from backend.modules.colored_logger import setup_logger
from pydantic import TypeAdapter

from backend.modules.models import Task
from backend.rules.custom_checks import check_duplicate_task, check_boxtrucks, check_preventative_maintenance

ALLOWED_TYPES = {"pull", "bring", "hook"}
logger = setup_logger(__name__)

TaskAdapter = TypeAdapter(Task)


def is_allowed_type(task_dict):
    """Check if the task type is allowed."""
    task_type = task_dict.get("type") or task_dict.get("yard_task_type")
    return task_type in ALLOWED_TYPES


def deduplicate_tasks(task_dicts):
    """Deduplicate tasks: keep only the oldest by (type, door)."""
    latest_by_type_door = {}
    for task_dict in task_dicts:
        typ = task_dict.get("type") or task_dict.get("yard_task_type")
        door = task_dict.get("door")
        key = (typ, door)
        if key not in latest_by_type_door:
            latest_by_type_door[key] = task_dict
        else:
            existing = latest_by_type_door[key]
            if (
                    task_dict.get("created_at") is not None and
                    existing.get("created_at") is not None and
                    task_dict["created_at"] < existing["created_at"]
            ):
                latest_by_type_door[key] = task_dict
    # Add tasks without a door (not deduped)
    deduped = list(latest_by_type_door.values())
    deduped += [t for t in task_dicts if t.get("door") is None]
    return deduped


def passes_business_rules(task, all_tasks):
    """Apply all business rules to a Task instance."""
    # Duplicate check
    allowed, reason = check_duplicate_task(task, all_tasks)
    if not allowed:
        return False, reason
    # Box truck check
    trailer_number = getattr(task, "trailer", "")
    if check_boxtrucks(trailer_number):
        if getattr(task, "type", None) == "pull":
            return False, f"Box trucks (trailer: {trailer_number}) are not allowed for pull tasks."
    # Preventative maintenance check
    yard_task_type = getattr(task, "yard_task_type", "")
    if check_preventative_maintenance(yard_task_type=yard_task_type):
        return False, f"Trailer {trailer_number} is flagged for preventative maintenance."
    return True, None


async def delete_task_external(task_id, task_store, session_manager=None):
    """Delete a task from the external system or just the local store."""
    if session_manager is not None:
        await session_manager.run_delete_task(task_id)
    else:
        await task_store.delete_task(task_id)


async def validate_and_store_task(task_dict, task_store, session_manager=None, all_tasks=None):
    """
    Validate and store a single task. If not valid, delete externally (if possible).
    Returns stored Task or None.
    """
    if not is_allowed_type(task_dict):
        logger.info(
            f"Deleting unwanted yard task type: {task_dict.get('type')} for case {task_dict.get('case_id') or task_dict.get('case_id')}")
        await delete_task_external(task_dict["id"], task_store, session_manager)
        return None
    try:
        task = TaskAdapter.validate_python(task_dict)
    except Exception as e:
        logger.error(
            f"Could not validate task: {task_dict}, error: {repr(e)}; details: {getattr(e, 'errors', lambda: None)()}")
        await delete_task_external(task_dict["id"], task_store, session_manager)
        return None
    allowed, reason = passes_business_rules(task, all_tasks or [])
    if not allowed:
        logger.info(f"Deleting task {task_dict.get('case_id')}: {reason}")
        await delete_task_external(task_dict["case_id"], task_store, session_manager)
        return None
    try:
        await task_store.upsert_task(task.model_dump())
        return task
    except Exception as e:
        logger.error(f"Could not store valid task: {task_dict}, error: {e}")
        return None


async def validate_and_store_tasks(task_dicts, task_store, session_manager=None):
    """
    Modular: Deduplicate, validate, and store multiple tasks.
    Invalid tasks are deleted externally if possible.
    Returns only the valid, stored Task instances.
    """
    deduped_task_dicts = deduplicate_tasks(task_dicts)
    valid_tasks = []
    # For duplicate checks, pass the current list of valid_tasks so far
    for task_dict in deduped_task_dicts:
        task = await validate_and_store_task(
            task_dict, task_store, session_manager=session_manager, all_tasks=valid_tasks
        )
        if task:
            valid_tasks.append(task)
    return valid_tasks
