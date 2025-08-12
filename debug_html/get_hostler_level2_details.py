import re
import json


def extract_task_fields_from_html(html: str):
    """
    Extracts fields from mergeBigData JSON in HTML <script> blocks.
    Returns a dict of relevant fields, or raises ValueError if not found.
    """
    for m in re.finditer(r"<script[^>]*>(.*?)</script>", html, re.DOTALL | re.MULTILINE):
        script_text = m.group(1)
        if "mergeBigData" in script_text:
            # Find the start of the mergeBigData call
            call_start = script_text.find("mergeBigData(")
            if call_start == -1:
                continue
            # Find the first '{' after mergeBigData(
            json_start = script_text.find('{', call_start)
            # Find the matching '})' or '});'
            # We'll look for the last '}' before ')'
            paren_close = script_text.find(')', json_start)
            brace_close = script_text.rfind('}', json_start, paren_close if paren_close != -1 else None)
            if json_start == -1 or brace_close == -1:
                continue
            data_json = script_text[json_start:brace_close + 1]
            try:
                data = json.loads(data_json)
            except Exception as e:
                raise ValueError(f"Failed to parse JSON from mergeBigData: {e}")
            pywork = data.get("pyWorkPage", {})
            meta = pywork.get("MetaData", {})
            return {
                "jockey_comments": pywork.get("Comments", ""),
                "drop_door": meta.get("DropDoor", ""),
                "trailer_type": meta.get("TrailerType", ""),
                "drop_off_zone": meta.get("ZoneTrailer", ""),
                "general_note": meta.get("pyDescription", "")
            }
    raise ValueError("Could not find mergeBigData JSON in any <script> block in HTML")


# Usage example:
if __name__ == "__main__":
    with open('step_1003.html', 'r') as reader:
        data = reader.read()
    fields = extract_task_fields_from_html(data)
    print(fields)
