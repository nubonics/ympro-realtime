from backend.rules.validation import passes_business_rules


def zero_door():
    all_tasks = [
        {"yard_task_type": "bring", "trailer_number": "MTY PUP", "door": "0"},
        {"yard_task_type": "pull", "trailer_number": "114", "door": "25"},
    ]
    new_task = {"yard_task_type": "bring", "trailer_number": "MTY PUP", "door": "0"}
    # Should allow because MTY is at door 0
    allowed, reason = passes_business_rules(new_task, all_tasks)
    print(allowed, reason)


zero_door()