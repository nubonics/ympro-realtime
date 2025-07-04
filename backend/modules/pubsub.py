import redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
TASK_CHANNEL = "tasks-events"


def publish_event(event_type, task):
    data = json.dumps({
        "event": event_type,  # "created", "updated", "deleted"
        "task": task
    })
    r.publish(TASK_CHANNEL, data)
