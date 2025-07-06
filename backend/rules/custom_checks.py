from backend.rules.helper import get_attr


def get_hook_trailer_set(task):
    # Collect all trailers present (upper-cased & stripped)
    trailers = []
    for attr in ("leadTrailer", "middleTrailer", "tailTrailer"):
        val = get_attr(task, attr, None)
        if val:
            trailers.append(val.upper().strip())
    return frozenset(trailers)


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
    task_type = get_attr(task, "yard_task_type")
    task_door = str(get_attr(task, "door"))
    trailer_number = str(get_attr(task, "trailer", "")).strip().upper()

    if task_type in ("pull", "bring"):
        # Skip duplication check if the door is 0, as these are notes for yard coordinators
        if task_door == 0 or task_door == "0":
            return True, None
        # Skip duplication check if the trailer number has `empty` or mty` in it as this is used for communication
        # between yard coordinators and hostlers
        if 'MTY' in trailer_number or 'EMPTY' in trailer_number:
            return True, None
        elif 'NOT IN PLAN' in trailer_number:
            return True, None
        elif 'OB' in trailer_number:
            return True, None
        elif not task_door or task_door == "None":
            return False, f"{task_type.title()} task must have a door."
        same = [
            t for t in all_tasks
            if get_attr(t, "yard_task_type") == task_type and str(get_attr(t, "door")) == task_door
        ]
    elif task_type == "hook":
        # Hook logic here... (implement if needed)
        return True, None
    else:
        same = [
            t for t in all_tasks
            if get_attr(t, "yard_task_type") == task_type and str(get_attr(t, "door")) == task_door
        ]

    if len(same) <= 1:
        return True, None

    def sort_key(x):
        created = get_attr(x, "created_at")
        if created:
            return created
        cid = get_attr(x, "case_id") or get_attr(x, "id") or ""
        try:
            return int(cid.replace("T-", ""))
        except Exception:
            return float('inf')

    try:
        oldest = min(same, key=sort_key)
    except Exception as e:
        return False, f"Duplicate check failed: {e}"

    def get_task_id(x):
        return get_attr(x, "id") or get_attr(x, "case_id") or "NO_ID"

    if get_task_id(task) == get_task_id(oldest):
        return True, None

    return False, f"Duplicate {task_type} task for door {task_door} is not allowed (only the oldest is kept)."
