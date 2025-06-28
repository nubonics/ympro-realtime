from ympro.backend.rules.custom_checks import check_duplicate_task, check_boxtrucks, check_preventative_maintenance


def check_task_rules(task, all_tasks):
    allowed, reason = check_duplicate_task(task, all_tasks)
    if not allowed:
        return False, reason

    trailer_number = getattr(task, "trailer", "")
    if check_boxtrucks(trailer_number):
        if getattr(task, "type", None) == "bring":
            return False, f"Box trucks (trailer: {trailer_number}) are not allowed for bring tasks."

    if check_preventative_maintenance(trailer_number):
        return False, f"Trailer {trailer_number} is flagged for preventative maintenance."

    return True, None


def validate_and_fix_tasks(tasks):
    unique_by_type_door = {}
    for t in tasks:
        if hasattr(t, "door"):
            key = (t.type, t.door)
            if key not in unique_by_type_door:
                unique_by_type_door[key] = t
            else:
                existing = unique_by_type_door[key]
                if t.id < existing.id:
                    unique_by_type_door[key] = t

    trailer_by_door = {}
    for t in unique_by_type_door.values():
        if hasattr(t, "door") and hasattr(t, "trailer"):
            d = t.door
            if d not in trailer_by_door:
                trailer_by_door[d] = t.trailer

    for t in unique_by_type_door.values():
        if hasattr(t, "door") and hasattr(t, "trailer"):
            t.trailer = trailer_by_door[t.door]

    remaining = [t for t in tasks if not hasattr(t, "door")]
    return list(unique_by_type_door.values()) + remaining
