import json
import hashlib
from datetime import datetime


def hash_result(result):
    as_bytes = json.dumps(result.model_dump(), sort_keys=True).encode("utf-8")
    return hashlib.sha256(as_bytes).hexdigest()


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
