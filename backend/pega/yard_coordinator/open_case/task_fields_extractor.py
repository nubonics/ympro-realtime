import re
import json
from lxml import html as lxml_html


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


def extract_mergeBigData_json(html):
    for m in re.finditer(r"<script[^>]*>(.*?)</script>", html, re.DOTALL | re.MULTILINE):
        script_text = m.group(1)
        idx = script_text.find("mergeBigData(")
        if idx == -1:
            continue
        start = script_text.find("{", idx)
        if start == -1:
            continue
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


def extract_selected_fields(html):
    data = extract_mergeBigData_json(html)
    pywork = data.get("pyWorkPage", {}) if data else {}
    meta = pywork.get("MetaData", {}) if pywork else {}

    def greedy_get(field):
        return (
                meta.get(field) or
                pywork.get(field) or
                find_field_recursively(pywork, field) or
                find_field_recursively(data, field) or
                ""
        )

    def greedy_case_info(field):
        return (
                pywork.get(field) or
                find_field_recursively(pywork, field) or
                find_field_recursively(data, field) or
                None
        )

    # Find resolved info (in any pxResults list)
    resolved_by = None
    resolved_status = None
    resolved_time = None

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

    history_events = collect_pxResults(data) if data else []
    for ev in history_events:
        msg = ev.get("$pxLocalized", {}).get("$pyMessageKey$pyCaption", "")
        if msg.startswith("Status changed to "):
            resolved_by = ev.get("pyPerformer")
            resolved_status = msg.replace("Status changed to ", "").rstrip(".")
            resolved_time = ev.get("pxTimeCreated")
            break

    result = {
        # Task fields
        "jockey_comments": greedy_get("Comments"),
        "drop_door": greedy_get("DropDoor"),
        "trailer_type": greedy_get("TrailerType"),
        "drop_off_zone": greedy_get("ZoneTrailer"),
        "general_note": greedy_get("pyDescription"),
        # Audit/case fields
        # "created_by": greedy_case_info("pxCreateOpName"),
        # "created_at": greedy_case_info("pxCreateDateTime"),
        # "updated_by": greedy_case_info("pxUpdateOpName"),
        # "updated_at": greedy_case_info("pxUpdateDateTime"),
        # "status": greedy_case_info("pyStatusWork"),
        # "resolved_by": resolved_by,
        # "resolved_status": resolved_status,
        # "resolved_time": resolved_time,
    }

    # Fallback: try hidden <input> fields if task fields are empty
    if not any([result["jockey_comments"], result["drop_door"], result["trailer_type"], result["drop_off_zone"],
                result["general_note"]]):
        tree = lxml_html.fromstring(html)

        def find_input_value(possible_names):
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

        result["jockey_comments"] = find_input_value(["Comments"])
        result["drop_door"] = find_input_value(["DropDoor", "drop_door"])
        result["trailer_type"] = find_input_value(["TrailerType", "trailer_type"])
        result["drop_off_zone"] = find_input_value(["ZoneTrailer", "drop_off_zone"])
        result["general_note"] = find_input_value(["pyDescription", "general_note"])

    return result
