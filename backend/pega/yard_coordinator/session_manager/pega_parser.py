import datetime
import json
import re
import time
import urllib
from urllib.parse import unquote

import xxhash
from dateparser import parse as date_parse
from lxml import html

from backend.modules.colored_logger import setup_logger
from backend.pega.yard_coordinator.session_manager.hostler_utils import extract_team_members_pd_key


logger = setup_logger(__name__)


def _parse_html(html_content: str):
    """
    Helper function that attempts to parse HTML content and returns the resulting tree.
    Logs any errors encountered.
    """
    try:
        tree = html.fromstring(html_content)
        logger.debug("HTML parsed successfully.")
        return tree
    except Exception as e:
        logger.error("Failed to parse HTML: %s", e)
        return None


def extract_pz_transaction_id(html_text: str) -> str | None:
    """
    Extracts the pzTransactionId value from a script tag that contains the metadata tree.
    It looks for a substring like "pzTransactionId=VALUE" and returns VALUE.
    """

    logger.info("Searching for pzTransactionId in the script text.")
    match = re.search(r"pzTransactionId=([^&\"\s]+)", html_text)
    if match:
        transaction_id = match.group(1)
        logger.info("Found pzTransactionId: %s", transaction_id)
        return transaction_id

    logger.warning("pzTransactionId not found in script text.")
    return None


def generate_fingerprint_token(seed=31):
    components = [
        {'key': 'userAgent',
         'value': 'Mozilla/5.0'},
        {'key': 'language', 'value': 'en-US'},
        {'key': 'deviceMemory', 'value': 8},
        {'key': 'hardwareConcurrency', 'value': 32},
        {'key': 'timezoneOffset', 'value': 480},
        {'key': 'timezone', 'value': 'America/Los_Angeles'},
        # {'key': 'localStorage', 'value': '1710719294951'},
        {'key': 'localStorage', 'value': str(int(time.time()))},
        {'key': 'cpuClass', 'value': 'not available'},
        {'key': 'platform', 'value': 'Win32'},
    ]
    values = ''.join(str(component['value']) for component in components)
    fingerprint_token = '{v2}' + xxhash.xxh128(values, seed=seed).hexdigest()
    return fingerprint_token


def parse_html(html_content: str):
    try:
        return html.fromstring(html_content)
    except Exception:
        return None


# --- Extract pzuiactionzzz (prefer grid selection token, fallback to button) ---
def extract_pzuiactionzzz_for_xfer_hostler_to_wb(html_text):
    # 1. Try data-postvalue-url (grid selection)
    tree = html.fromstring(html_text)
    for el in tree.xpath("//*[contains(@data-postvalue-url, 'pzuiactionzzz=')]"):
        val = el.attrib.get('data-postvalue-url') or ""
        match = re.search(r'pzuiactionzzz=([A-Za-z0-9%*=]+)', val)
        if match:
            return match.group(1)
    # 2. Fallback to first button with data-click (modal actions)
    for el in tree.xpath("//button[contains(@data-click, 'pzuiactionzzz=')]"):
        data_click = el.attrib.get('data-click') or ""
        match = re.search(r'pzuiactionzzz=([A-Za-z0-9%*=]+)', data_click)
        if match:
            return match.group(1)
    return None


def extract_pzuiactionzzz(html_text: str) -> str | None:
    """
    Extracts pzuiactionzzz value from raw HTML containing Pega's mergeBigData JSON blob.
    """
    try:
        match = re.search(r'"pzuiactionzzz"\s*:\s*"([^"]+)"', html_text)
        if match:
            return match.group(1)

        # fallback: look for "$pxActionString": { ... } and search keys
        px_action_match = re.search(r'\$pxActionString"\s*:\s*{(.*?)}', html_text, re.DOTALL)
        if px_action_match:
            inner_json = px_action_match.group(1)
            action_match = re.search(r'"pzuiactionzzz"\s*:\s*"([^"]+)"', inner_json)
            return action_match.group(1) if action_match else None
    except Exception as e:
        logger.warning(f"[Step 1] Error extracting pzuiactionzzz: {e}")

    return None


def extract_section_ids(html_content: str) -> str:
    tree = parse_html(html_content)
    elements_with_id = tree.xpath("//*[@containedSectionID]")
    contained_ids = [elem.get("containedSectionID").strip() for elem in elements_with_id if
                     elem.get("containedSectionID")]
    if len(contained_ids) >= 2:
        return f"{contained_ids[0]}:{contained_ids[1]}:"
    return ""


def extract_hostler_info(html_content, verbose=False):
    tree = html.fromstring(html_content)
    rows = tree.xpath("//tr[contains(@class, 'cellCont')]")
    hostlers = []
    for row in rows:
        try:
            elements = row.xpath(".//strong[@data-userId] | .//strong[@data-name]")
            if not elements:
                if verbose:
                    continue
            name_elem = elements[0]
            hostler_name = name_elem.text_content().strip()
            checker_id = int(name_elem.get("data-userid") or 0)
            tasks_elements = row.xpath(".//td[@data-attribute-name='Tasks']")
            number_of_moves = 0
            if tasks_elements:
                span_elements = tasks_elements[0].xpath(".//span")
                if span_elements:
                    try:
                        number_of_moves = int(span_elements[0].text_content().strip())
                    except Exception:
                        pass
            hostlers.append({
                "name": hostler_name,
                "checker_id": checker_id,
                "moves": number_of_moves
            })
        except Exception:
            continue
    return hostlers


def extract_hostler_view_details(html_content):
    tree = html.fromstring(html_content)
    assigned_to_elements = tree.xpath("//span[contains(concat(' ', normalize-space(@class), ' '), ' heading_2 ')]")
    assigned_to = assigned_to_elements[0].text_content().strip() if assigned_to_elements else "Unknown"
    tasks = []
    rows = tree.xpath("//tr[contains(concat(' ', normalize-space(@class), ' '), ' cellCont ')]")
    for row in rows:
        try:
            case_id_elements = row.xpath(".//a")
            if not case_id_elements:
                continue
            case_id = case_id_elements[0].text_content().strip()
            task_type_elements = row.xpath(".//td[@data-attribute-name='Yard Task Type']")
            # type_of_trailer = task_type_elements[0].text_content().strip() if task_type_elements else ""
            # No, type_of_trailer is not what is above as this would require the trailer number and conditions
            #  to determine what length of trailer this is and if it has a liftgate or not
            yard_task_type = task_type_elements[0].text_content().strip() if task_type_elements else ""
            if 'pull' in yard_task_type.lower():
                yard_task_type = 'pull'
            elif 'bring' in yard_task_type.lower():
                yard_task_type = 'bring'
            elif 'hook' in yard_task_type.lower():
                yard_task_type = 'hook'
            elif 'prevent' in yard_task_type.lower() or 'maintenance' in yard_task_type.lower():
                yard_task_type = 'preventive_maintenance'
            elif 'yard chat' in yard_task_type.lower():
                yard_task_type = 'yard_chat'
            else:
                raise Exception(
                    f'Unknown yard task type: {yard_task_type} for case {case_id}\nextract_hostler_view_details')
            create_date_elements = row.xpath(".//td[@data-attribute-name='Create Date']")
            create_date_str = create_date_elements[0].text_content().strip() if create_date_elements else ""
            try:
                created_at = date_parse(create_date_str)
            except Exception:
                created_at = datetime.datetime.utcnow()
            trailer_no_elements = row.xpath(".//td[@data-attribute-name='Trailer No']")
            trailer_number = trailer_no_elements[0].text_content().strip() if trailer_no_elements else ""
            door_no_elements = row.xpath(".//td[@data-attribute-name='Door No']")
            door = door_no_elements[0].text_content().strip() if door_no_elements else ""
            status_elements = row.xpath(".//td[@data-attribute-name='Status']")
            status = status_elements[0].text_content().strip() if status_elements else ""
            if status == "Open-InProgress":
                status = "PENDING"
            task = {
                "case_id": case_id,
                "trailer_number": trailer_number,
                "door": door,
                "assigned_to": assigned_to,
                "status": status,
                "locked": False,
                "created_at": created_at,
                "order": 0,
                "drop_off_zone": None,
                "general_note": None,
                "type_of_trailer": None,
                "drop_location": None,
                "hostler_comments": None,
                "trailer": trailer_number,
                "yard_task_type": yard_task_type,
            }
            tasks.append(task)
        except Exception:
            continue
    return {"assigned_to": assigned_to, "tasks": tasks}


def extract_workbasket_tasks(html_content: str, assigned_to: str = "workbasket"):
    tree = html.fromstring(html_content)
    rows = tree.xpath(
        "//tr[contains(@class, 'cellCont') and (contains(@class, 'oddRow') or contains(@class, 'evenRow'))]")
    tasks = []
    for row in rows:
        cells = row.xpath(".//td")
        if len(cells) < 7:
            continue
        case_id_list = cells[0].xpath(".//a/text()")
        case_id = case_id_list[0].strip() if case_id_list else cells[0].text_content().strip()
        yard_task_type = cells[1].text_content().strip()
        # inside your function:
        if 'pull' in yard_task_type.lower():
            yard_task_type = 'pull'
        elif 'bring' in yard_task_type.lower():
            yard_task_type = 'bring'
        elif 'hook' in yard_task_type.lower():
            yard_task_type = 'hook'
        elif 'prevent' in yard_task_type.lower() or 'maintenance' in yard_task_type.lower():
            yard_task_type = 'preventive_maintenance'
        elif 'yard chat' in yard_task_type.lower():
            yard_task_type = 'yard_chat'
        else:
            raise Exception(
                f'Unknown yard task type: {yard_task_type} for case {case_id}\nextract_workbasket_tasks')
        trailer_no = cells[2].text_content().strip()
        door_no = cells[3].text_content().strip()
        create_date_str = cells[4].text_content().strip()
        status = "PENDING"
        created_at = date_parse(create_date_str)
        if created_at is None:
            created_at = datetime.datetime.utcnow()
        task = {
            "case_id": case_id,
            "trailer_number": trailer_no,
            "door": door_no,
            "assigned_to": assigned_to,
            "status": status,
            "locked": False,
            "created_at": created_at,
            "order": 0,
            "drop_off_zone": None,
            "general_note": None,
            "type_of_trailer": None,
            "drop_location": None,
            "hostler_comments": None,
            "trailer": trailer_no,
            "yard_task_type": yard_task_type,
        }
        tasks.append(task)
    return tasks


def extract_session_data(html_content: str):
    tree = html.fromstring(html_content)
    csrf_elements = tree.xpath("//input[@id='XCSRFToken']")
    csrf_token = csrf_elements[0].get("value") if csrf_elements else None

    base_refs_elements = tree.xpath("//td[@base_ref]")
    base_refs = [td.get("base_ref") for td in base_refs_elements]

    pzHarnessID_elements = tree.xpath("//input[@id='pzHarnessID']")
    pzHarnessID = pzHarnessID_elements[0].get("value") if pzHarnessID_elements else None

    pzTransactionId_elements = tree.xpath("//input[@id='pzTransactionId']")
    pzTransactionId = pzTransactionId_elements[0].get("value") if pzTransactionId_elements else None

    return {
        "csrf_token": csrf_token,
        "base_refs": base_refs,
        "pzHarnessID": pzHarnessID,
        "pzTransactionId": pzTransactionId,  # <-- NEW
    }


def get_pzTransactionId_for_create_task(html_content: str) -> str | None:
    tree = parse_html(html_content)
    xpath_expr = "//script[contains(text(), 'pega.ui.jittemplate.addMetadataTree')]"
    script_elements = tree.xpath(xpath_expr)
    if not script_elements:
        return None
    script_text = script_elements[0].text
    if not script_text:
        return None
    match = re.search(r"pzTransactionId=([^&\"\s]+)", script_text)
    return match.group(1) if match else None


def get_PD_pzRenderFeedContext_for_create_task(html_content: str) -> str | None:
    tree = parse_html(html_content)
    xpath_expr = "//input[contains(@name, 'PD_pzRenderFeedContext')]"
    input_elements = tree.xpath(xpath_expr)
    if not input_elements:
        return None
    name_attr = input_elements[0].get("name")
    match = re.search(r"(\$PD_pzRenderFeedContext_[^$]+)", name_attr)
    return match.group(1) if match else None


def get_PD_pzFeedParams_for_create_task(html_content: str) -> str | None:
    tree = parse_html(html_content)
    xpath_expr = "//div[@id='AJAXCT']"
    div_elements = tree.xpath(xpath_expr)
    if not div_elements:
        return None
    data_json = div_elements[0].get("data-json")
    if not data_json:
        return None
    try:
        data = json.loads(data_json)
    except Exception:
        return None
    initial = data.get("Initial", {})
    for key in initial:
        if key.startswith("D_pzFeedParams"):
            return key.replace("D_", "PD_", 1)
    return None


def extract_pzuiactionzzz_for_create_task(html_content: str) -> str | None:
    tree = parse_html(html_content)
    if tree is None:
        return None
    xpath_expr = "//script[contains(text(), '$pxActionString') and contains(text(), 'pzuiactionzzz')]"
    script_elements = tree.xpath(xpath_expr)
    for script in script_elements:
        script_text = script.text_content()
        match = re.search(r'pzuiactionzzz\\u003d([^"]+)', script_text)
        if match:
            return urllib.parse.unquote(match.group(1))
    return None


def get_row_page(base_ref, page_index=None):
    """
    Returns the row_page for a paginated request.
    If page_index is None, returns the root.
    If page_index is given, appends .pxResults(N)
    """
    root = re.sub(r"\.pxResults\(\d+\)$", "", base_ref)
    if page_index and page_index > 1:
        return f"{root}.pxResults({page_index})"
    return root


def extract_grid_action_fields(html_text):
    tree = html.fromstring(html_text)

    # 1. selected_row_id (assignment row)
    selected_tr = tree.xpath("//tr[contains(@id, '$PD_FetchWorkListAssignments_') and contains(@id, '$ppxResults$l')]")
    selected_row_id = selected_tr[0].get("id") if selected_tr else None

    # 2. pyPropertyTarget (assignment row)
    pyprop_input = tree.xpath(
        "//input[@type='checkbox' and contains(@name, '$PD_FetchWorkListAssignments_') and contains(@name, '$ppxResults') and contains(@name, '$ppySelected')]")
    pyPropertyTarget = pyprop_input[0].get("name") if pyprop_input else None

    # 3. base_ref (hostler-level, prefer base_ref, fallback prim_page)
    base_ref = None
    base_ref_elems = tree.xpath("//*[@name='base_ref' and @base_ref]")
    for elem in base_ref_elems:
        val = elem.get("base_ref")
        if val and val.strip():
            base_ref = val.strip()
            break
    if not base_ref:
        base_ref_elems = tree.xpath("//*[@base_ref]")
        for elem in base_ref_elems:
            val = elem.get("base_ref")
            if val and val.strip():
                base_ref = val.strip()
                break
    if not base_ref:
        prim_page_elems = tree.xpath("//*[@prim_page]")
        for elem in prim_page_elems:
            val = elem.get("prim_page")
            if val and val.strip():
                base_ref = val.strip()
                break

    # 4. context_page (from hashed-dp-page)
    context_elem = tree.xpath("//*[@hashed-dp-page]")
    context_page = None
    if context_elem:
        page = context_elem[0].get("hashed-dp-page")
        if page:
            context_page = f"{page}(1)"
    else:
        ds_elem = tree.xpath("//*[@dataSource]")
        for elem in ds_elem:
            ds = elem.get("dataSource", "")
            m = re.search(r'(D_FetchWorkListAssignments_[^\.]+)\.pxResults', ds)
            if m:
                context_page = f"{m.group(1)}.pxResults(1)"
                break

    # 5. pzuiactionzzz
    postval_div = tree.xpath("//div[@data-postvalue-url]")
    pzuiactionzzz = None
    if postval_div:
        urlval = postval_div[0].get("data-postvalue-url")
        m = re.search(r"pzuiactionzzz=([^&]+)", urlval)
        if m:
            pzuiactionzzz = unquote(m.group(1))

    # 6. pzHarnessID (not present in sample, but search for id starting with HID)
    hid_elem = tree.xpath("//*[starts-with(@id, 'HID')]")
    pzHarnessID = hid_elem[0].get("id") if hid_elem else None

    # 7. row_page (derived from base_ref)
    row_page = get_row_page(base_ref) if base_ref else None

    # 8. fetch_worklist_pd_key (new integration)
    fetch_worklist_pd_key = extract_fetch_worklist_pd_key(html_text)

    # 9. team_members_pd_key
    team_members_pd_key = extract_team_members_pd_key(html_text)

    # 10. strIndexInList
    strIndexInList = extract_str_index_in_list(html_text)

    return {
        "selected_row_id": selected_row_id,
        "pyPropertyTarget": pyPropertyTarget,
        "base_ref": base_ref,
        "context_page": context_page,
        "pzuiactionzzz": pzuiactionzzz,
        "pzHarnessID": pzHarnessID,
        "row_page": row_page,
        "fetch_worklist_pd_key": fetch_worklist_pd_key,
        "team_members_pd_key": team_members_pd_key,
        "strIndexInList": strIndexInList,
    }


def extract_str_index_in_list(html_text):
    """
    Extracts the strIndexInList value from the grid row.
    Typically this is found as PL_INDEX, index, or a similar attribute on the <tr> for the assignment.
    Returns the first found value as a string, or None if not found.
    """
    tree = html.fromstring(html_text)
    # Find the main grid assignment row (usually contains OAArgs, PL_INDEX, etc.)
    tr = tree.xpath("//tr[contains(@class, 'cellCont') and (@PL_INDEX or @pl_index or @index)]")
    for elem in tr:
        idx = elem.get("PL_INDEX") or elem.get("pl_index") or elem.get("index")
        if idx is not None:
            return str(idx)
    # Fallback: try to extract from the id if it encodes the index (e.g., $ppxResults$l12)
    rows = tree.xpath("//tr[contains(@id, '$ppxResults$l')]")
    if rows:
        m = re.search(r"\$ppxResults\$l(\d+)", rows[0].get("id", ""))
        if m:
            return m.group(1)
    return None


def extract_fetch_worklist_pd_key(html_text):
    from lxml import html
    tree = html.fromstring(html_text)
    # Look for a grid table with PL_PROP attribute
    table = tree.xpath("//table[@PL_PROP]")
    if table:
        return table[0].attrib.get("PL_PROP")
    # Fallback: regex
    import re
    m = re.search(r"PL_PROP=['\"]([^'\"]+)['\"]", html_text)
    if m:
        return m.group(1)
    return None


def extract_task_fields_from_html(html: str):
    """
    Extracts fields from mergeBigData JSON in HTML <script> blocks.
    Returns a dict of relevant fields, or raises ValueError if not found.

    - created_by: $pxCreateOpName$pyButtonLabel
    - updated_by: last event in history with "$pyMessageKey$pyCaption" == "Task details manually updated"
    - updated_by_timestamp: from that event
    - resolved_by: event with "$pyMessageKey$pyCaption" starting with "Status changed to "
    - resolved_by_status: status string from that event
    - resolved_by_timestamp: from that event
    - case_status: $$pyStatusWork$pyCaption
    """
    # Patterns for simple string fields (fallbacks)
    create_op_pattern = r'\$pxCreateOpName\$pyButtonLabel"\s*:\s*"([^"]*)"'
    create_op_match = re.search(create_op_pattern, html)
    create_op_value = create_op_match.group(1) if create_op_match else None

    # Pattern for $$pyStatusWork$pyCaption
    status_work_pattern = r'\$\$pyStatusWork\$pyCaption"\s*:\s*"([^"]*)"'
    status_work_match = re.search(status_work_pattern, html)
    status_work_value = status_work_match.group(1) if status_work_match else None

    # Try to extract mergeBigData JSON from a <script> block
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

            # Main pyWorkPage extraction
            pywork = data.get("pyWorkPage", {})
            meta = pywork.get("MetaData", {})

            # Try to find a history list anywhere in the data (recursively)
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

            # Find updated_by (last event with "$pyMessageKey$pyCaption" == "Task details manually updated")
            updated_by_event = None
            resolved_by_event = None
            if history_list:
                for event in history_list:
                    msg = event.get("$pxLocalized", {}).get("$pyMessageKey$pyCaption", "")
                    if msg == "Task details manually updated":
                        updated_by_event = event  # keep overwriting to get the last
                    elif msg.startswith("Status changed to "):
                        resolved_by_event = event  # (should only be one)

            # Compose outputs
            out = {
                "jockey_comments": pywork.get("Comments", ""),
                "drop_door": meta.get("DropDoor", ""),
                "trailer_type": meta.get("TrailerType", ""),
                "drop_off_zone": meta.get("ZoneTrailer", ""),
                "general_note": meta.get("pyDescription", ""),
                "created_by": create_op_value,
                "case_status": status_work_value,
                # History events:
                "updated_by": None,
                "updated_by_timestamp": None,
                "resolved_by": None,
                "resolved_by_status": None,
                "resolved_by_timestamp": None,
            }
            if updated_by_event:
                out["updated_by"] = updated_by_event.get("pyPerformer")
                out["updated_by_timestamp"] = updated_by_event.get("pxTimeCreated")
            if resolved_by_event:
                out["resolved_by"] = resolved_by_event.get("pyPerformer")
                msg = resolved_by_event.get("$pxLocalized", {}).get("$pyMessageKey$pyCaption", "")
                # Extract status string
                status = msg.replace("Status changed to ", "").rstrip(".")
                out["resolved_by_status"] = status
                out["resolved_by_timestamp"] = resolved_by_event.get("pxTimeCreated")
            return out
    raise ValueError("Could not find mergeBigData JSON in any <script> block in HTML")
