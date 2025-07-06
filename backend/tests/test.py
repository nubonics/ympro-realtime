import datetime

from custom_checks import check_duplicate_task


data = [{"case_id": "T-34393597", "trailer_number": "NOT IN PLAN", "door": "0", "assigned_to": "workbasket", "status": "PENDING", "locked": False, "created_at": datetime.datetime(2025, 7, 3, 21, 15), "order": 0, "drop_off_zone": None, "general_note": None, "type_of_trailer": None, "drop_location": None, "hostler_comments": None, "door": "0", "trailer": "NOT IN PLAN", "id": "T-34393597", "yard_task_type": "bring"}, {"case_id": "T-34403824", "trailer_number":"123456", "door": "1", "assigned_to": "workbasket", "status": "PENDING", "locked": False, "created_at": datetime.datetime(2025, 7, 5, 0, 56), "order": 0, "drop_off_zone": None, "general_note": None, "type_of_trailer": None, "drop_location": None, "hostler_comments": None, "door": "1", "trailer": "123456", "id": "T-34403824", "yard_task_type": "bring"}, {"case_id": "T-34403825", "trailer_number": "234567", "door": "1", "assigned_to": "workbasket", "status": "PENDING", "locked": False, "created_at": datetime.datetime(2025, 7, 5, 0, 57), "order": 0, "drop_off_zone": None, "general_note": None, "type_of_trailer": None, "drop_location": None, "hostler_comments": None, "door": "1", "trailer": "234567", "id": "T-34403825", "yard_task_type": "bring"}]

for x in range(len(data)):
    y = check_duplicate_task(
            task=data[x],
            all_tasks=data
        )
    print(f"Task {data[x]['id']} check result: {y}")