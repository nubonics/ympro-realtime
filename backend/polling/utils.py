import json
import hashlib


def hash_result(result):
    as_bytes = json.dumps(result.model_dump(), sort_keys=True).encode("utf-8")
    return hashlib.sha256(as_bytes).hexdigest()
