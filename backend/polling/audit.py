import json
import asyncio
import logging
import os

AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH", "./poller_audit.log")
logger = logging.getLogger("poller.audit")

def audit_log(event, task, reason=None):
    entry = {
        "event": event,
        "task_id": getattr(task, "id", None),
        "assigned_to": getattr(task, "assigned_to", None),
        "type": getattr(task, "type", None),
        "door": getattr(task, "door", None),
        "trailer": getattr(task, "trailer", None),
        "reason": reason,
        "timestamp": asyncio.get_event_loop().time()
    }
    try:
        with open(AUDIT_LOG_PATH, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        logger.error(f"Failed to write audit log: {e}")