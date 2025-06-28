def check_boxtrucks(trailer_number: str) -> bool:
    """
    Returns True if trailer_number is a box truck (starts with 19, 10, or contains SPEC).
    """
    if not trailer_number:
        return False
    trailer_number = trailer_number.upper()
    return (
            trailer_number.startswith("19")
            or trailer_number.startswith("10")
            or "SPEC" in trailer_number
    )


def check_preventative_maintenance(yard_task_type: str):
    """
    Returns True if 'Preventative' is in the yard task type (case-insensitive).
    """
    if not yard_task_type:
        return None
    return "PREVENTATIVE" in yard_task_type.upper()


def check_duplicate_task(task, all_tasks):
    """
    Checks if there is already a task of the same type and door (but different id).
    Returns (allowed: bool, reason: Optional[str])
    """
    if hasattr(task, "door") and hasattr(task, "type"):
        for t in all_tasks:
            if (
                    hasattr(t, "door") and t.door == task.door and
                    hasattr(t, "type") and t.type == task.type and
                    t.id != task.id
            ):
                return False, f"Duplicate {task.type} task for door {task.door} is not allowed."
    return True, None
