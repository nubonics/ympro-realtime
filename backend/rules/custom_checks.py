from backend.rules.helper import get_attr


def get_hook_trailer_set(task):
    trailers = []
    for attr in ("leadTrailer", "middleTrailer", "tailTrailer"):
        val = get_attr(task, attr, None)
        if val:
            trailers.append(val.upper().strip())
    return frozenset(trailers)


def check_boxtrucks(trailer_number: str) -> bool:
    if not trailer_number:
        return False
    trailer_number = trailer_number.upper()
    trailer_number = trailer_number.strip("'\"")
    # print("Checking boxtruck:", trailer_number)  # <-- Debug print
    # print("Checking boxtruck:", repr(trailer_number))  # <-- Debug print
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


def is_duplicate_mty_task(new_task, all_tasks):
    # Use get_attr for both trailer/trailer_number and door
    trailer = (get_attr(new_task, "trailer_number") or get_attr(new_task, "trailer") or "").upper()
    door = get_attr(new_task, "door")

    # SKIP duplicate check for door 0 (special case for notes)
    if door == 0 or door == "0":
        return False

    # If this is an MTY/EMPTY task, check for another active MTY/EMPTY at the same door
    if "MTY" in trailer or "EMPTY" in trailer:
        for t in all_tasks:
            t_trailer = (get_attr(t, "trailer_number") or get_attr(t, "trailer") or "").upper()
            t_door = get_attr(t, "door")
            if t_door == door and ("MTY" in t_trailer or "EMPTY" in t_trailer):
                return True
    return False


def check_duplicate_task(task, all_tasks):
    task_type = get_attr(task, "yard_task_type")
    task_door = str(get_attr(task, "door"))
    trailer_number = str(get_attr(task, "trailer", "") or get_attr(task, "trailer_number", "")).strip().upper()

    if task_type in ("pull", "bring"):
        # Skip duplication check if the door is 0, as these are notes for yard coordinators
        if task_door == "0" or task_door == 0:
            return True, None
        # Check for duplicate MTY/EMPTY
        if is_duplicate_mty_task(task, all_tasks):
            return False, f"Duplicate MTY/EMPTY task for door {task_door}"
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
