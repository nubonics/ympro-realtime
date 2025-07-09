from backend.rules.validation import passes_business_rules


def test_zero_door():
    all_tasks = [
        {"yard_task_type": "bring", "trailer_number": "MTY PUP", "door": "0"},
        {"yard_task_type": "pull", "trailer_number": "114", "door": "25"},
    ]
    new_task = {"yard_task_type": "bring", "trailer_number": "MTY PUP", "door": "0"}
    # Should allow because MTY is at door 0
    allowed, reason = passes_business_rules(new_task, all_tasks)
    assert allowed


def test_zero_door2():
    all_tasks = [
        {"yard_task_type": "bring", "trailer_number": "MTY PUP", "door": 0},
        {"yard_task_type": "pull", "trailer_number": "114", "door": "25"},
    ]
    new_task = {"yard_task_type": "bring", "trailer_number": "NOT IN PLAN", "door": 0}
    # Should allow because MTY is at door 0
    allowed, reason = passes_business_rules(new_task, all_tasks)
    assert allowed


def test_mty_trailer_duplicate_different_doors():
    all_tasks = [
        {"yard_task_type": "bring", "trailer_number": "MTY PUP", "door": "21"},
        {"yard_task_type": "pull", "trailer_number": "114", "door": "25"},
    ]
    new_task = {"yard_task_type": "bring", "trailer_number": "MTY PUP", "door": "25"}
    # Should allow because MTY is at different doors
    allowed, reason = passes_business_rules(new_task, all_tasks)
    assert allowed


def test_mty_trailer_same_door():
    all_tasks = [
        {"yard_task_type": "bring", "trailer_number": "MTY PUP", "door": "21"},
        {"yard_task_type": "pull", "trailer_number": "114", "door": "25"},
    ]
    new_task = {"yard_task_type": "bring", "trailer_number": "MTY PUP", "door": "21"}

    # Should block because MTY is at same door
    allowed, reason = passes_business_rules(new_task, all_tasks)
    assert not allowed


def test_mty_trailer_duplicate_same_door():
    all_tasks = [
        {"yard_task_type": "pull", "trailer_number": "MTY PUP", "door": "21"},
    ]
    new_task = {"yard_task_type": "pull", "trailer_number": "MTY PUP", "door": "21"}
    # Should block because MTY is at same door
    allowed, reason = passes_business_rules(new_task, all_tasks)
    assert not allowed


def test_boxtruck_pull_prevented1():
    all_tasks = [{"yard_task_type": "pull", "trailer_number": "19283", "door": "21"}, ]
    new_task = {"yard_task_type": "pull", "trailer_number": "19302", "door": "25"}
    # Should block because box trucks are not allowed for pull tasks
    allowed, reason = passes_business_rules(new_task, all_tasks)
    assert not allowed


def test_boxtruck_pulls_prevented2():
    new_task = {"yard_task_type": "pull", "trailer_number": "SPEC1234", "door": "23"}
    allowed, reason = passes_business_rules(new_task, [])
    assert not allowed


def test_boxtruck_pulls_prevented3():
    all_tasks = [{"yard_task_type": "pull", "trailer_number": "10302", "door": "21"}]
    new_task = {"yard_task_type": "pull", "trailer_number": "10385", "door": "22"}
    # Should block because box trucks are not allowed for pull tasks
    allowed, reason = passes_business_rules(new_task, all_tasks)
    assert not allowed


def test_preventive_maintenance_prevention():
    all_tasks = [
        {"yard_task_type": "preventive maintenance", "trailer_number": "528546", "door": "21"},
    ]
    new_task = {"yard_task_type": "preventive maintenance", "trailer_number": "529000", "door": "25"}
    # Should block because trailer is flagged for preventative maintenance
    allowed, reason = passes_business_rules(new_task, all_tasks)
    assert not allowed


def test_empty_pull_task():
    all_tasks = []
    new_task = {"yard_task_type": "pull", "trailer_number": "EMPTY PUP", "door": "23"}
    # Should allow because it's an empty pull task
    allowed, reason = passes_business_rules(new_task, all_tasks)
    assert allowed
