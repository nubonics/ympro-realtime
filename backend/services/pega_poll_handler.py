from backend.rules.validation import check_task_rules
from backend.services.storage import get_redis, store_task, remove_task, emit_to_frontend
from backend.services.external_api import delete_task_external

async def handle_poll_payload(payload):
    """
    Orchestrates validation, storage, emission, and external deletion.

    Args:
        payload (dict): The poller payload, expected to have format:
            {
                "hostlers": [
                    {
                        "id": ...,
                        "name": ...,
                        "tasks": [ ... ]
                    },
                    ...
                ]
            }
    """
    redis = await get_redis()

    # Flatten all tasks
    all_tasks = []
    for hostler in payload.get("hostlers", []):
        all_tasks.extend(hostler.get("tasks", []))

    for task in all_tasks:
        allowed, reason = check_task_rules(task, all_tasks)
        if allowed:
            print(f"Task {task['id']} valid! Emitting to frontend and storing in Redis.")
            await store_task(redis, task)
            await emit_to_frontend(redis, task)
        else:
            print(f"Task {task['id']} invalid: {reason} Removing from Redis and deleting on external site.")
            await remove_task(redis, task)
            await delete_task_external(task)

    await redis.close()