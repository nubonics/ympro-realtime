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
    if not yard_task_type:
        return None
    s = yard_task_type.upper()
    return "PREVENTIVE" in s or "PREVENTATIVE" in s


def check_duplicate_task(task, all_tasks):
    same = [
        t for t in all_tasks
        if t.yard_task_type == task.yard_task_type and t.door == task.door
    ]
    if len(same) <= 1:
        return True, None
    oldest = min(same, key=lambda x: x.created_at)
    if task.id == oldest.id:
        return True, None
    return False, f"Duplicate {task.yard_task_type} task for door {task.door} is not allowed (only the oldest is kept)."
