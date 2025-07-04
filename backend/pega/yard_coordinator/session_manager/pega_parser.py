import datetime
import re
import time
import urllib

import xxhash
from dateparser import parse as date_parse
from lxml import html

from backend.modules.colored_logger import setup_logger

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
            else:
                raise Exception(f'Unknown yard task type: {yard_task_type} for case {case_id}\nextract_hostler_view_details')
            create_date_elements = row.xpath(".//td[@data-attribute-name='Create Date']")
            create_date_str = create_date_elements[0].text_content().strip() if create_date_elements else ""
            try:
                created_at = date_parse(create_date_str)
            except Exception:
                created_at = datetime.datetime.utcnow()
            trailer_no_elements = row.xpath(".//td[@data-attribute-name='Trailer No']")
            trailer_number = trailer_no_elements[0].text_content().strip() if trailer_no_elements else ""
            door_no_elements = row.xpath(".//td[@data-attribute-name='Door No']")
            door_number = door_no_elements[0].text_content().strip() if door_no_elements else ""
            status_elements = row.xpath(".//td[@data-attribute-name='Status']")
            status = status_elements[0].text_content().strip() if status_elements else ""
            if status == "Open-InProgress":
                status = "PENDING"
            task = {
                "case_id": case_id,
                "trailer_number": trailer_number,
                "door_number": door_number,
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
                "door": door_number,
                "trailer": trailer_number,
                "id": case_id,
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
        if 'pull' in yard_task_type.lower():
            yard_task_type = 'pull'
        elif 'bring' in yard_task_type.lower():
            yard_task_type = 'bring'
        elif 'hook' in yard_task_type.lower():
            yard_task_type = 'hook'
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
            "door_number": door_no,
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
            "door": door_no,
            "trailer": trailer_no,
            "id": case_id,
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
