def extract_task_fields_from_html(html: str):
    """
    Extracts fields from mergeBigData JSON in HTML <script> blocks.
    Returns a dict of relevant fields, or raises ValueError if not found.
    """
    import re
    # Pattern for "$pxCreateOpName$pyButtonLabel"
    create_op_pattern = r'\$pxCreateOpName\$pyButtonLabel"\s*:\s*"([^"]*)"'
    create_op_match = re.search(create_op_pattern, html)
    create_op_value = create_op_match.group(1) if create_op_match else None

    # Pattern for "$$pyStatusWork$pyCaption"
    status_work_pattern = r'\$pyStatusWork\$pyCaption"\s*:\s*"([^"]*)"'
    status_work_match = re.search(status_work_pattern, html)
    status_work_value = status_work_match.group(1) if status_work_match else None

    # Patter for $pyPerformer$pyCaption
    performer_pattern = r'\$pyPerformer\$pyCaption"\s*:\s*"([^"]*)"'
    performer_match = re.search(performer_pattern, html)
    performer_value = performer_match.group(1) if performer_match else None


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
                "general_note": meta.get("pyDescription", ""),
                "created_by": create_op_value,  # $pxCreateOpName$pyButtonLabel
                "updated_by": create_op_value,  # $pxCreateOpName$pyButtonLabel
                "resolved_by": performer_value,  # $pyPerformer$pyCaption
                "case_status": status_work_value,  # $pyStatusWork$pyCaption
            }
    raise ValueError("Could not find mergeBigData JSON in any <script> block in HTML")