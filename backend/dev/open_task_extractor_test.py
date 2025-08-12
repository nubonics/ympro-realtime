import re
import json
from lxml import html as lxml_html


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
    raise ValueError("mergeBigData({ ... }) block not found or not valid JSON")


def get_case_info(html):
    data = extract_mergeBigData_json(html)
    pywork = data.get("pyWorkPage", {})
    created_by = pywork.get("pxCreateOpName")
    created_at = pywork.get("pxCreateDateTime")
    updated_by = pywork.get("pxUpdateOpName")
    updated_at = pywork.get("pxUpdateDateTime")
    status = pywork.get("pyStatusWork")
    # Find history list
    history = []
    for k, v in data.items():
        if isinstance(v, dict) and "pxResults" in v:
            for ev in v["pxResults"]:
                if (
                        "pyPerformer" in ev
                        and "pxTimeCreated" in ev
                        and "pyMessageKey" in ev
                ):
                    history.append(ev)
    # Optionally, extract last resolved by and status
    resolved_event = next((h for h in history if
                           h.get("$pxLocalized", {}).get("$pyMessageKey$pyCaption", "").startswith(
                               "Status changed to ")), None)
    resolved_by = resolved_event.get("pyPerformer") if resolved_event else None
    resolved_status = None
    resolved_time = None
    if resolved_event:
        msg = resolved_event.get("$pxLocalized", {}).get("$pyMessageKey$pyCaption", "")
        resolved_status = msg.replace("Status changed to ", "").rstrip(".")
        resolved_time = resolved_event.get("pxTimeCreated")
    return {
        "created_by": created_by,
        "created_at": created_at,
        "updated_by": updated_by,
        "updated_at": updated_at,
        "status": status,
        "resolved_by": resolved_by,
        "resolved_status": resolved_status,
        "resolved_time": resolved_time,
        # "history": history
    }


def find_field_recursively(d, field_name):
    """Recursively search for a field in any dict/list structure."""
    if isinstance(d, dict):
        if field_name in d:
            return d[field_name]
        for v in d.values():
            result = find_field_recursively(v, field_name)
            if result is not None:
                return result
    elif isinstance(d, list):
        for item in d:
            result = find_field_recursively(item, field_name)
            if result is not None:
                return result
    return None


def extract_task_fields_from_html(html: str):
    # Fallbacks from HTML (for created_by, case_status)
    create_op_pattern = r'\$pxCreateOpName\$pyButtonLabel"\s*:\s*"([^"]*)"'
    create_op_match = re.search(create_op_pattern, html)
    fallback_created_by = create_op_match.group(1) if create_op_match else None

    status_work_pattern = r'\$\$pyStatusWork\$pyCaption"\s*:\s*"([^"]*)"'
    status_work_match = re.search(status_work_pattern, html)
    fallback_case_status = status_work_match.group(1) if status_work_match else None

    # Try to extract from mergeBigData JSON
    for m in re.finditer(r"<script[^>]*>(.*?)</script>", html, re.DOTALL | re.MULTILINE):
        script_text = m.group(1)
        if "mergeBigData" in script_text:
            call_start = script_text.find("mergeBigData(")
            if call_start == -1:
                continue
            json_start = script_text.find('{', call_start)
            if json_start == -1:
                continue
            # Bracket-matching
            brace_count = 0
            in_string = False
            string_char = ''
            escape = False
            for i, c in enumerate(script_text[json_start:], start=json_start):
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
                            data_json = script_text[json_start:i + 1]
                            break
            else:
                continue
            try:
                data = json.loads(data_json)
            except Exception as e:
                raise ValueError(f"Failed to parse JSON from mergeBigData: {e}")

            pywork = data.get("pyWorkPage", {})
            meta = pywork.get("MetaData", {})

            # Find history list anywhere
            def find_history_list(obj):
                if isinstance(obj, list):
                    if obj and isinstance(obj[0], dict) and "pyPerformer" in obj[0] and "pxTimeCreated" in obj[0]:
                        return obj
                    for item in obj:
                        found = find_history_list(item)
                        if found:
                            return found
                elif isinstance(obj, dict):
                    for v in obj.values():
                        found = find_history_list(v)
                        if found:
                            return found
                return None

            history_list = find_history_list(data)
            updated_by_event = None
            resolved_by_event = None
            if history_list:
                for event in history_list:
                    msg = event.get("$pxLocalized", {}).get("$pyMessageKey$pyCaption", "")
                    if msg == "Task details manually updated":
                        updated_by_event = event
                    elif msg.startswith("Status changed to "):
                        resolved_by_event = event
                if not updated_by_event and history_list:
                    updated_by_event = history_list[0]
            if not updated_by_event:
                updated_by_event = {
                    "pyPerformer": pywork.get("pxUpdateOpName"),
                    "pxTimeCreated": pywork.get("pxUpdateDateTime"),
                }

            created_by = pywork.get("pxCreateOpName") or fallback_created_by
            case_status = pywork.get("pyStatusWork") or fallback_case_status

            # Try best-effort recursive for drop_door etc
            drop_door = meta.get("DropDoor") or find_field_recursively(pywork, "DropDoor") or find_field_recursively(
                data, "DropDoor") or ""
            trailer_type = meta.get("TrailerType") or find_field_recursively(pywork,
                                                                             "TrailerType") or find_field_recursively(
                data, "TrailerType") or ""
            drop_off_zone = meta.get("ZoneTrailer") or find_field_recursively(pywork,
                                                                              "ZoneTrailer") or find_field_recursively(
                data, "ZoneTrailer") or ""
            general_note = meta.get("pyDescription") or find_field_recursively(pywork,
                                                                               "pyDescription") or find_field_recursively(
                data, "pyDescription") or ""

            return {
                "jockey_comments": pywork.get("Comments", ""),
                "drop_door": drop_door,
                "trailer_type": trailer_type,
                "drop_off_zone": drop_off_zone,
                "general_note": general_note,
                "created_by": created_by,
                "case_status": case_status,
                "updated_by": updated_by_event.get("pyPerformer") if updated_by_event else None,
                "updated_by_timestamp": updated_by_event.get("pxTimeCreated") if updated_by_event else None,
                "resolved_by": resolved_by_event.get("pyPerformer") if resolved_by_event else None,
                "resolved_by_status": (
                    resolved_by_event.get("$pxLocalized", {}).get("$pyMessageKey$pyCaption", "").replace(
                        "Status changed to ", "").rstrip(".")
                    if resolved_by_event else None
                ),
                "resolved_by_timestamp": resolved_by_event.get("pxTimeCreated") if resolved_by_event else None,
            }

    # If not found in JSON, try lxml fallback for hidden fields
    tree = lxml_html.fromstring(html)

    def find_input_value(possible_names):
        # Return value of input where name or id matches any of possible_names (case-insensitive)
        for name in possible_names:
            el = tree.xpath(
                f"//input[translate(@name,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='{name.lower()}']")
            if el and el[0].get("value"):
                return el[0].get("value")
            el = tree.xpath(
                f"//input[translate(@id,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='{name.lower()}']")
            if el and el[0].get("value"):
                return el[0].get("value")
        return ""

    return {
        "jockey_comments": find_input_value(["Comments"]),
        "drop_door": find_input_value(["DropDoor", "drop_door"]),
        "trailer_type": find_input_value(["TrailerType", "trailer_type"]),
        "drop_off_zone": find_input_value(["ZoneTrailer", "drop_off_zone"]),
        "general_note": find_input_value(["pyDescription", "general_note"]),
        "created_by": fallback_created_by,
        "case_status": fallback_case_status,
        "updated_by": None,
        "updated_by_timestamp": None,
        "resolved_by": None,
        "resolved_by_status": None,
        "resolved_by_timestamp": None,
    }


if __name__ == "__main__":
    # Replace with your file path
    with open('../../debug_html/step_1003.html', encoding="utf-8") as f:
        html = f.read()
    res = get_case_info(html)
    import pprint;

    pprint.pprint(res)
    x = extract_task_fields_from_html(html)
    print(x)
