import re
import json


def extract_mergeBigData_json(html):
    for m in re.finditer(r"<script[^>]*>(.*?)</script>", html, re.DOTALL | re.MULTILINE):
        script_text = m.group(1)
        idx = script_text.find("mergeBigData(")
        if idx == -1:
            continue
        start = script_text.find("{", idx)
        if start == -1:
            continue

        # Bracket matching algorithm
        brace_count = 0
        in_string = False
        string_char = ""
        escape = False
        for i, c in enumerate(script_text[start:], start=start):
            if in_string:
                if escape:
                    escape = False
                elif c == "\\":
                    escape = True
                elif c == string_char:
                    in_string = False
            else:
                if c in ('"', "'"):
                    in_string = True
                    string_char = c
                elif c == "{":
                    brace_count += 1
                elif c == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        json_str = script_text[start:i + 1]
                        try:
                            return json.loads(json_str)
                        except json.JSONDecodeError as e:
                            print("DEBUG: JSON decode error:", e)
                            print("DEBUG: JSON excerpt:\n", json_str[:500])
                            raise
    return None


def find_field_recursively(d, field_name):
    """Recursively search for a field in any dict/list structure."""
    if isinstance(d, dict):
        if field_name in d and d[field_name] not in [None, ""]:
            return d[field_name]
        for v in d.values():
            result = find_field_recursively(v, field_name)
            if result not in [None, ""]:
                return result
    elif isinstance(d, list):
        for item in d:
            result = find_field_recursively(item, field_name)
            if result not in [None, ""]:
                return result
    return None


def collect_pxResults(obj):
    results = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "pxResults" and isinstance(v, list):
                results.extend(v)
            else:
                results.extend(collect_pxResults(v))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(collect_pxResults(item))
    return results


def get_case_info(html):
    data = extract_mergeBigData_json(html)

    def greedy(field):
        # Deep search in the whole JSON!
        return find_field_recursively(data, field) if data else None

    created_by = greedy("pxCreateOpName")
    created_at = greedy("pxCreateDateTime")
    updated_by = greedy("pxUpdateOpName")
    updated_at = greedy("pxUpdateDateTime")
    status = greedy("pyStatusWork")

    # Find resolved event anywhere
    resolved_by = None
    resolved_status = None
    resolved_time = None
    history = []

    if data:
        history_events = collect_pxResults(data)
        for ev in history_events:
            msg = ev.get("$pxLocalized", {}).get("$pyMessageKey$pyCaption", "")
            if msg.startswith("Status changed to "):
                resolved_by = ev.get("pyPerformer")
                resolved_status = msg.replace("Status changed to ", "").rstrip(".")
                resolved_time = ev.get("pxTimeCreated")
            # Collect history
            if "pyPerformer" in ev and "pxTimeCreated" in ev and "pyMessageKey" in ev:
                history.append(ev)

    return {
        "created_by": created_by,
        "created_at": created_at,
        "updated_by": updated_by,
        "updated_at": updated_at,
        "status": status,
        "resolved_by": resolved_by,
        "resolved_status": resolved_status,
        "resolved_time": resolved_time,
        # "history": history,
    }
