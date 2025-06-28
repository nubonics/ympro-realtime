import asyncio
import datetime
import re
import time
import urllib
from os import getenv, makedirs
from os.path import exists
from typing import List, Dict, Any

import httpx
import xxhash
from dateparser import parse
from lxml import html
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.hostler_models import Hostler
from backend.models.task_models import Task
from backend.models.task_update_models import HostlerUpdateBroadcast
from backend.routes.backend_to_frontend_connection.connection_manager_singleton import get_connection_manager
from task_classes.create_task import CreateTask
from task_classes.delete_task import DeleteTask
from task_classes.transfer_task import TransferTask
from backend.utils.database.db import get_db
from backend.utils.database.db import database
from backend.colored_logger import setup_logger

logger = setup_logger(__name__)


class LoginError(Exception):
    """Raised when login fails."""
    pass


class PegaTaskSessionManager:
    def __init__(self):
        # Let the client handle cookies automatically.
        self.last_broadcast_payload = None
        self.sectionIDList = None
        self.pzuiactionzzz = None
        self.last_login_time = None
        self.base_url = None
        self.async_client = httpx.AsyncClient(follow_redirects=False)
        self.base_refs = []
        self.pzHarnessID = ""
        self.csrf_token = None
        self.redirected_url = None
        self.details_url = None  # URL from the GET after redirect to be used in subsequent POSTs
        self.login_response_text = None
        self.debug_save_html = bool(getenv('PEGA_DEBUG_SAVE_HTML'))
        self.hostler_data_memory = {}  # In-memory storage for hostler details
        self.fingerprint_token = self.generate_fingerprint_token()
        self.updated_hostler_summary = False

    @staticmethod
    def save_html_to_file(content, step: int, enabled: bool = False):
        if not enabled:
            return
        try:
            file_path = f"debug_html/step_{step}.html"
            if not exists("debug_html"):
                makedirs("debug_html", exist_ok=True)
            if isinstance(content, str):
                content = content.encode("utf-8")
            with open(file_path, "wb") as file:
                file.write(content)
            logger.debug(f"Saved HTML content for step {step} to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save HTML content for step {step}: {e}")

    def should_relogin(self, max_age_hours: int = 11) -> bool:
        """
        Returns True if the session manager needs to re-login because the last login
        time is older than 'max_age_hours'. If no successful login has occurred, also returns True.
        """
        if self.last_login_time is None:
            # We haven't logged in yet, so definitely need to log in.
            return True

        elapsed = datetime.datetime.utcnow() - self.last_login_time
        return elapsed > datetime.timedelta(hours=max_age_hours)

    @staticmethod
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

    def extract_pzuiactionzzz(self, html_content: str) -> str | None:
        """
        Extracts the pzuiactionzzz value from a script tag in the provided HTML.
        Looks for the pattern: pzuiactionzzz\u003d<value> (until the next double quote),
        URL‑decodes the raw value, and returns it.
        """
        logger.info("Starting extraction of pzuiactionzzz from HTML content.")
        tree = self._parse_html(html_content)
        if tree is None:
            return None

        xpath_expr = "//script[contains(text(), '$pxActionString') and contains(text(), 'pzuiactionzzz')]"
        script_elements = tree.xpath(xpath_expr)
        if not script_elements:
            logger.warning("No script elements found with xpath: %s", xpath_expr)
            return None

        for script in script_elements:
            script_text = script.text_content()
            logger.debug("Script text (first 100 chars): %s", script_text[:100])
            match = re.search(r'pzuiactionzzz\\u003d([^"]+)', script_text)
            if match:
                raw_value = match.group(1)
                logger.info("Found raw pzuiactionzzz value: %s", raw_value)
                decoded_value = urllib.parse.unquote(raw_value)
                logger.info("Decoded pzuiactionzzz value: %s", decoded_value)
                return decoded_value

        logger.warning("pzuiactionzzz value not found in any script element.")
        return None

    async def login(self):
        try:
            logger.info("Starting login process...")
            initial_url = "https://ymg.estes-express.com/prweb/app/default"
            initial_response = await self.async_client.get(initial_url, follow_redirects=True)
            self.base_url = initial_response.url
            logger.debug(f'initial response headers: {initial_response.headers}')
            logger.debug(f'initial_response url: {initial_response.url}')
            self.save_html_to_file(initial_response.content, step=1, enabled=self.debug_save_html)
            # redirected_url = initial_response.headers.get("Location")
            redirected_url = initial_response.url
            logger.debug(f'redirected location url: {redirected_url}')
            # if not redirected_url:
            #     logger.critical("No 'Location' header found in the initial response.")
            #     raise LoginError("Missing redirect location.")
            # if not redirected_url.startswith("http"):
            #     redirected_url = initial_url.rstrip("/") + redirected_url
            self.redirected_url = redirected_url
            logger.info(f"Redirected URL: {redirected_url}")

            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            }
            self.async_client.headers.update(headers)
            response_1 = await self.async_client.get(redirected_url)
            logger.debug(f'response_1 url: {response_1.url}')
            self.save_html_to_file(response_1.content, step=2, enabled=self.debug_save_html)
            # Capture the URL from response_1 for later use
            self.details_url = str(response_1.url)
            logger.info(f"Details URL captured: {self.details_url}")

            captcha_url = f"{redirected_url}?pyActivity=Code-Security.pyGenerateCaptcha"
            logger.debug(f'captcha_url url: {captcha_url}')
            captcha_response = await self.async_client.get(captcha_url, headers=headers, follow_redirects=True)
            self.save_html_to_file(captcha_response.content, step=3, enabled=self.debug_save_html)

            login_data = {
                "pzAuth": "guest",
                "UserIdentifier": getenv('PEGA_USERNAME'),
                "Password": getenv('PEGA_PASSWORD'),
                "pyActivity=Code-Security.Login": ""
            }
            logger.info("Submitting login credentials...")
            login_response = await self.async_client.post(redirected_url, data=login_data, follow_redirects=True)
            self.save_html_to_file(login_response.content, step=4, enabled=self.debug_save_html)
            self.login_response_text = login_response.text
            self.pzuiactionzzz = self.extract_pzuiactionzzz(html_content=self.login_response_text)
            self.sectionIDList = self.extract_section_ids(html_content=self.login_response_text)

            await self.extract_session_data(login_response)
            logger.info("Login process completed successfully.")
            self.last_login_time = datetime.datetime.utcnow()

        except Exception as e:
            logger.error(f"Login failed: {e}")
            raise LoginError("Login failed") from e

    async def extract_session_data(self, response):
        try:
            logger.info("Extracting session data...")
            tree = html.fromstring(response.text)
            csrf_elements = tree.xpath("//input[@id='XCSRFToken']")
            if csrf_elements:
                self.csrf_token = csrf_elements[0].get("value")
                logger.debug(f"Extracted CSRF token: {self.csrf_token}")
            else:
                logger.warning("CSRF token not found in the response.")

            base_refs_elements = tree.xpath("//td[@base_ref]")
            self.base_refs = [td.get("base_ref") for td in base_refs_elements]
            if not self.base_refs:
                logger.warning("No base_refs found in the response.")

            pzHarnessID_elements = tree.xpath("//input[@id='pzHarnessID']")
            if not pzHarnessID_elements:
                raise ValueError("pzHarnessID not found in the HTML.")
            self.pzHarnessID = pzHarnessID_elements[0].get("value")
            logger.info(f"Session data extracted: {len(self.base_refs)} base_refs, pzHarnessID={self.pzHarnessID}")
        except Exception as e:
            logger.error(f"Error extracting session data: {e}")
            raise LoginError("Failed to extract session data.") from e

    @staticmethod
    def extract_hostler_view_details(html_content):
        try:
            tree = html.fromstring(html_content)
            assigned_to_elements = tree.xpath(
                "//span[contains(concat(' ', normalize-space(@class), ' '), ' heading_2 ')]")
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
                    type_of_trailer = task_type_elements[0].text_content().strip() if task_type_elements else ""

                    create_date_elements = row.xpath(".//td[@data-attribute-name='Create Date']")
                    create_date_str = create_date_elements[0].text_content().strip() if create_date_elements else ""
                    try:
                        created_at = parse(create_date_str)
                    except Exception as e:
                        logger.error("Error parsing create date '%s': %s", create_date_str, e)
                        created_at = datetime.datetime.utcnow()

                    trailer_no_elements = row.xpath(".//td[@data-attribute-name='Trailer No']")
                    trailer_number = trailer_no_elements[0].text_content().strip() if trailer_no_elements else ""

                    door_no_elements = row.xpath(".//td[@data-attribute-name='Door No']")
                    door_number = door_no_elements[0].text_content().strip() if door_no_elements else ""

                    status_elements = row.xpath(".//td[@data-attribute-name='Status']")
                    status = status_elements[0].text_content().strip() if status_elements else ""
                    # Normalize status: convert "Open-InProgress" to "PENDING"
                    if status == "Open-InProgress":
                        status = "PENDING"

                    # Optionally, if your UI expects fields 'door' and 'trailer', you could add them here:
                    task = Task(
                        case_id=case_id,
                        trailer_number=trailer_number,
                        door_number=door_number,
                        assigned_to=assigned_to,
                        status=status,
                        locked=False,
                        created_at=created_at,
                        order=0,
                        drop_off_zone=None,
                        general_note=None,
                        type_of_trailer=type_of_trailer,
                        drop_location=None,
                        hostler_comments=None,
                    )
                    tasks.append(task)
                except Exception as e:
                    logger.error("Error processing row: %s", e)
                    continue
            # Return a payload with consistent field names.
            # If desired, you can also include duplicate keys for backward compatibility:
            # For example, copy door_number to door, trailer_number to trailer.
            normalized_tasks = []
            for t in tasks:
                task_dict = t.dict() if hasattr(t, "dict") else t.__dict__
                # Optionally add alias keys:
                task_dict["door"] = task_dict.get("door_number", "")
                task_dict["trailer"] = task_dict.get("trailer_number", "")
                normalized_tasks.append(task_dict)

            logger.debug(f'extract_view_details: assigned_to:{assigned_to} tasks: {normalized_tasks}')

            return {"assigned_to": assigned_to, "tasks": normalized_tasks}
        except Exception as e:
            logger.error("Error parsing HTML content: %s", e)
            return {"assigned_to": "Unknown", "tasks": []}

    @staticmethod
    def extract_hostler_info(html_content, verbose=False):
        """
        Extracts hostler information from the HTML table rows.

        Returns a list of dictionaries, e.g.:
          [
             {"name": "Manning, Troy", "checker_id": "222925", "moves": 2},
             ...
          ]
        """
        tree = html.fromstring(html_content)
        rows = tree.xpath("//tr[contains(@class, 'cellCont')]")
        hostlers = []
        for row in rows:
            try:
                # Look for the <strong> element with either data-userId or data-name.
                elements = row.xpath(".//strong[@data-userId] | .//strong[@data-name]")
                if not elements:
                    if verbose:
                        logger.debug("Skipping row: Missing hostler name.")
                    continue
                name_elem = elements[0]
                hostler_name = name_elem.text_content().strip()
                # Extract the checker_id from the "data-userId" attribute.
                checker_id = int(name_elem.get("data-userid"))
                if not checker_id:
                    # Optionally, fall back to an id attribute.
                    checker_id = name_elem.get("id")
                # Extract the number of moves from the cell with attribute Tasks.
                tasks_elements = row.xpath(".//td[@data-attribute-name='Tasks']")
                number_of_moves = 0
                if tasks_elements:
                    span_elements = tasks_elements[0].xpath(".//span")
                    if span_elements:
                        try:
                            number_of_moves = int(span_elements[0].text_content().strip())
                        except Exception as inner_e:
                            if verbose:
                                logger.error(
                                    f"Error converting tasks text to int for hostler {hostler_name}: {inner_e}")
                hostlers.append({
                    "name": hostler_name,
                    "checker_id": checker_id,
                    "moves": number_of_moves
                })
            except Exception as e:
                if verbose:
                    logger.error(f"Error processing row: {e}")
                continue
        return hostlers

    @staticmethod
    async def upsert_hostler(db: AsyncSession, hostler_data: dict):
        """
        Performs an upsert (add or update) for a single hostler record.
        """
        stmt = select(Hostler).where(Hostler.checker_id == hostler_data["checker_id"])
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing:
            # Update fields if necessary.
            existing.name = hostler_data["name"]
            existing.moves = hostler_data["moves"]
            db.add(existing)
            logger.info(f"Updated hostler (checker_id: {hostler_data['checker_id']}).")
        else:
            new_hostler = Hostler(
                name=hostler_data["name"],
                checker_id=hostler_data["checker_id"],
                moves=hostler_data["moves"]
            )
            db.add(new_hostler)
            logger.info(f"Added new hostler (checker_id: {hostler_data['checker_id']}).")
        await db.commit()

    @staticmethod
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

    async def flatten_and_upsert_tasks(self, payload_data):
        # Convert to dict if it's a Pydantic model
        if hasattr(payload_data, "dict"):
            payload_data = payload_data.dict()
        all_tasks = []
        for hostler_item in payload_data.get("hostlers", []):
            for t in hostler_item.get("tasks", []):
                all_tasks.append(t)
        await self.upsert_tasks(all_tasks)

    @staticmethod
    async def upsert_tasks(tasks: List[Dict[str, Any]]) -> None:
        """
        Upsert (create or update) tasks in the DB based on their 'id' field.
        """
        async with database.transaction():
            for tdict in tasks:
                task_id = tdict.get("id")
                if task_id is None:
                    continue

                stmt = select(Task).where(Task.__table__.c.id == task_id)
                existing_task = await database.fetch_one(stmt)

                trailer_number = tdict.get("trailer_number", "") or ""
                poller_override = True
                if "mty" in trailer_number.lower() or "move" in trailer_number.lower():
                    poller_override = False

                status = tdict.get("status", "PENDING")
                if status == "Open-InProgress":
                    status = "PENDING"

                if existing_task:
                    update_query = Task.__table__.update().where(
                        Task.__table__.c.id == task_id
                    ).values(
                        trailer_number=trailer_number,
                        door_number=tdict.get("door_number", existing_task["door_number"]),
                        assigned_to=tdict.get("assigned_to", existing_task["assigned_to"]),
                        status=status,
                        locked=tdict.get("locked", existing_task["locked"]),
                        order=tdict.get("order", existing_task["order"]),
                        case_id=tdict.get("case_id", existing_task["case_id"]),
                        drop_off_zone=tdict.get("drop_off_zone", existing_task["drop_off_zone"]),
                        general_note=tdict.get("general_note", existing_task["general_note"]),
                        type_of_trailer=tdict.get("type_of_trailer", existing_task["type_of_trailer"]),
                        drop_location=tdict.get("drop_location", existing_task["drop_location"]),
                        hostler_comments=tdict.get("hostler_comments", existing_task["hostler_comments"]),
                        poller_can_override=poller_override,
                    )
                    await database.execute(update_query)
                else:
                    created_at = datetime.datetime.utcnow()
                    insert_query = Task.__table__.insert().values(
                        id=task_id,
                        trailer_number=trailer_number,
                        door_number=tdict.get("door_number", "UNKNOWN"),
                        assigned_to=tdict.get("assigned_to"),
                        status=status,
                        locked=tdict.get("locked", False),
                        created_at=created_at,
                        order=tdict.get("order", 0),
                        case_id=tdict.get("case_id", "UNKNOWN"),
                        drop_off_zone=tdict.get("drop_off_zone"),
                        general_note=tdict.get("general_note"),
                        type_of_trailer=tdict.get("type_of_trailer"),
                        drop_location=tdict.get("drop_location"),
                        hostler_comments=tdict.get("hostler_comments"),
                        poller_can_override=poller_override,
                    )
                    await database.execute(insert_query)

    @staticmethod
    async def upsert_hostler_summary(hostler_name: str, moves: int, checker_id: str) -> dict:
        stmt = select(Hostler).where(Hostler.__table__.c.name == hostler_name)
        record = await database.fetch_one(stmt)
        if record:
            update_query = Hostler.__table__.update().where(
                Hostler.__table__.c.name == hostler_name
            ).values(
                moves=moves,
                checker_id=checker_id
            )
            await database.execute(update_query)
            record = await database.fetch_one(stmt)
        else:
            insert_query = Hostler.__table__.insert().values(
                name=hostler_name,
                moves=moves,
                checker_id=checker_id
            )
            await database.execute(insert_query)
            record = await database.fetch_one(stmt)
        return record

    async def fetch_all_pega_tasks(self):
        params = {
            "pzTransactionId": "",
            "pzFromFrame": "",
            "pzPrimaryPageName": "pyPortalHarness",
            "AJAXTrackID": "1",
            "eventSrcSection": "Data-Portal.TeamMembersGrid",
        }
        connection_manager = get_connection_manager()

        # Extract workbasket data.
        response = await self.fetch_workbasket_data()
        workbasket_data = self.extract_workbasket_tasks(html_content=response.text)
        logger.debug(f'workbasket data: {workbasket_data}')
        await connection_manager.broadcast_event("workbasket_update", workbasket_data)

        # Extract hostler summary data.
        # This will extract hostler summary data every polling_interval seconds instead of just at login
        # hostler_summary_data = await self.fetch_hostler_summary_data()
        # await connection_manager.broadcast_event("hostler_summary_update", hostler_summary_data)

        # Update hostler summary from the initial login response.
        if self.updated_hostler_summary is False:
            if self.login_response_text:
                hostlers_summary = self.extract_hostler_info(self.login_response_text)
                logger.debug(f'Hostlers Summary Data: {hostlers_summary}')
                for hostler in hostlers_summary:
                    await self.upsert_hostler_summary(
                        hostler_name=hostler["name"],
                        moves=hostler["moves"],
                        checker_id=hostler["checker_id"],
                    )
                del hostlers_summary
                self.updated_hostler_summary = True

        # Define a coroutine to fetch & process details for one base_ref.
        async def fetch_hostler_details(counter: int, base_ref: str) -> Dict[str, Any]:
            step_count = counter + 4

            location_params = {
                "pyActivity": "pzPrepareAssignment",
                "UITemplatingStatus": "Y",
                "NewTaskStatus": "DisplayUserWorkList",
                "TaskIndex": "",
                "StreamType": "Rule-HTML-Section",
                "FieldError": "",
                "FormError": "",
                "pyCustomError": "",
                "bExcludeLegacyJS": "true",
                "ModalSection": "pzModalTemplate",
                "modalStyle": "",
                "IgnoreSectionSubmit": "true",
                "bInvokedFromControl": "true",
                "BaseReference": "",
                "isModalFlowAction": "true",
                "bIsModal": "true",
                "bIsOverlay": "false",
                "StreamClass": "Rule-HTML-Section",
                "UITemplatingScriptLoad": "true",
                "ActionSection": "pzModalTemplate",
                "rowPage": base_ref,
                "GridAction": "true",
                "BaseThread": "STANDARD",
                "pzHarnessID": self.pzHarnessID,
            }
            location_params_str = "&".join(f"{key}={value}" for key, value in location_params.items())

            data = {
                "pyActivity": "pzRunActionWrapper",
                "rowPage": base_ref,
                "Location": location_params_str,
                "PagesToCopy": base_ref.split(".pxResults")[0],
                "pzHarnessID": self.pzHarnessID,
                "UITemplatingStatus": "N",
                "inStandardsMode": "true",
                "eventSrcSection": "Data-Portal.TeamMembersGrid",
                "pzActivity": "pzPerformGridAction",
                "skipReturnResponse": "true",
                "pySubAction": "runAct",
            }

            headers = {
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "DNT": "1",
                "Origin": "https://ymg.estes-express.com",
                "Pragma": "no-cache",
                "Referer": self.details_url,
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0",
                "X-Requested-With": "XMLHttpRequest",
                "pzBFP": self.fingerprint_token,
                "pzCTkn": self.csrf_token if self.csrf_token else "",
                "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
            }

            logger.info(f"Fetching hostler details for base_ref: {base_ref} (Counter: {counter})")
            response = await self.async_client.post(
                self.details_url, headers=headers, data=data, params=params, follow_redirects=True
            )
            self.save_html_to_file(response.content, step=step_count, enabled=self.debug_save_html)

            # Extract hostler view details.
            hostler_details = self.extract_hostler_view_details(response.text)
            hostler_name = hostler_details.get("assigned_to", "Unknown")

            # Process tasks into dicts.
            tasks = hostler_details.get("tasks", [])
            logger.debug(f'hostler_details: {hostler_details}')
            tasks_as_dicts = []
            for t in tasks:
                if isinstance(t, dict):
                    d = t
                elif hasattr(t, "dict"):
                    d = t.dict()
                else:
                    d = t.__dict__
                d.pop("_sa_instance_state", None)
                if "id" not in d:
                    d["id"] = d.get("case_id", None)
                # Normalize aliases for backward compatibility.
                d["door"] = d.get("door_number", "")
                d["trailer"] = d.get("trailer_number", "")
                if "yardType" not in d and "type_of_trailer" in d:
                    d["yardType"] = d["type_of_trailer"]
                tasks_as_dicts.append(d)

            logger.debug(f'tasks_as_dicts: {tasks_as_dicts}')

            filtered_tasks = self.filter_out_tasks(tasks_as_dicts=tasks_as_dicts)

            logger.debug(f'filtered_tasks: {filtered_tasks}')

            # Save details to in-memory storage.
            self.hostler_data_memory[hostler_name] = filtered_tasks
            logger.info(f"Stored hostler details for {hostler_name} in memory.")

            # Return the payload for this hostler.
            return {
                "id": f"detail_{counter}",
                "name": hostler_name,
                "tasks": filtered_tasks
            }

        # Build a list of coroutines up to max_count.
        fetch_coroutines = [
            fetch_hostler_details(counter, base_ref)
            for counter, base_ref in enumerate(self.base_refs, start=1)
            # if counter <= max_count
        ]

        # Run all fetches concurrently.
        hostler_payloads = await asyncio.gather(*fetch_coroutines, return_exceptions=False)

        aggregated_payload = {"hostlers": hostler_payloads}

        # Apply the door_number filter on the aggregated payload.
        aggregated_payload = self.filter_aggregated_payload(aggregated_payload)

        logger.debug(f'aggregated_payload: {aggregated_payload}')

        # Validate payload with Pydantic if desired.
        try:
            validated_payload = HostlerUpdateBroadcast(**aggregated_payload)
        except Exception as e:
            logger.error(f"Pydantic validation error: {e}")
            validated_payload = aggregated_payload

        # Upsert all tasks in one DB session.
        await self.flatten_and_upsert_tasks(payload_data=validated_payload)

        await connection_manager.broadcast_event("hostler_update", aggregated_payload)

        # Compare with the last broadcast payload:
        if self.last_broadcast_payload == aggregated_payload:
            logger.info("Hostler data unchanged, skipping websocket broadcast.")
        else:
            await connection_manager.broadcast_event("hostler_update", aggregated_payload)
            logger.info("Fetched hostler details for all processed base_refs and notified frontend.")
            logger.info(f"Hostler data memory: {self.hostler_data_memory}")
            # Update the last broadcast payload
            self.last_broadcast_payload = aggregated_payload
        return True

    # @staticmethod
    def extract_workbasket_tasks(self, html_content: str, assigned_to: str = "workbasket"):
        """
        Extracts workbasket tasks from the given HTML content and returns them in a format
        matching the hostler data memory format.

        Each extracted task will have the following keys:
          - case_id
          - trailer_number
          - door_number
          - assigned_to
          - status (normalized to "PENDING")
          - locked (False)
          - created_at (a datetime object parsed from the "Create Date" column)
          - order (0)
          - drop_off_zone (None)
          - general_note (None)
          - type_of_trailer (taken from the "Yard Task Type" column)
          - drop_location (None)
          - hostler_comments (None)
          - door (same as door_number)
          - trailer (same as trailer_number)
          - id (same as case_id)
          - yardType (same as type_of_trailer)
        """
        try:
            self.save_html_to_file(content=html_content, step=100, enabled=self.debug_save_html)
            tree = html.fromstring(html_content)
            # Look for rows that have either 'oddRow' or 'evenRow' in their class.
            rows = tree.xpath(
                "//tr[contains(@class, 'cellCont') and (contains(@class, 'oddRow') or contains(@class, 'evenRow'))]"
            )

            tasks = []
            for row in rows:
                cells = row.xpath(".//td")
                if len(cells) < 7:
                    continue  # Skip rows that do not have enough cells

                # Extract Case ID (from an <a> tag if available)
                case_id_list = cells[0].xpath(".//a/text()")
                case_id = case_id_list[0].strip() if case_id_list else cells[0].text_content().strip()

                # Extract other fields
                yard_task_type = cells[1].text_content().strip()
                trailer_no = cells[2].text_content().strip()
                door_no = cells[3].text_content().strip()
                create_date_str = cells[4].text_content().strip()
                # The update date (cells[5]) is available but not used here.
                # Normalize any status text to "PENDING" (per sample hostler data memory)
                status = "PENDING"

                # Parse the create date string. If parsing fails, use current UTC time.
                created_at = parse(create_date_str)
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
                    "type_of_trailer": yard_task_type,
                    "drop_location": None,
                    "hostler_comments": None,
                    "door": door_no,
                    "trailer": trailer_no,
                    "id": case_id,
                    "yardType": yard_task_type,
                }
                tasks.append(task)
            return tasks
        except Exception as e:
            logger.debug(f'Problem extracting workbasket data: {e}')
            return None

    async def fetch_hostler_summary_data(self):
        params = {
            'pzFromFrame': '',
            'pzPrimaryPageName': 'pyPortalHarness',
            'AJAXTrackID': '1',
        }

        data = {
        "D_TeamMembersByWorkGroupPpxResults1colWidthGBL": "",
        "D_TeamMembersByWorkGroupPpxResults1colWidthGBR": "",
        "pzuiactionzzz": self.pzuiactionzzz,
        "PreActivitiesList": "",
        "sectionParam": "",
        "ActivityParams": "%3D",
        "$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType": "WORK",
        "$OCompositeGadget": "",
        "$OControlMenu": "",
        "$ODesktopWrapperInclude": "",
        "$ODeterminePortalTop": "",
        "$ODynamicContainerFrameLess": "",
        "$ODynamicLayout": "",
        "$ODynamicLayoutCell": "",
        "$OEvalDOMScripts_Include": "",
        "$OForm": "",
        "$OGapIdentifier": "",
        "$OGridInc": "",
        "$OHarness": "",
        "$OHarnessStaticJSEnd": "",
        "$OHarnessStaticJSStart": "",
        "$OHarnessStaticScriptsClientValidation": "",
        "$OHarnessStaticScriptsExprCal": "",
        "$OLaunchFlow": "",
        "$OMenuBar": "",
        "$OMenuBarOld": "",
        "$OMobileAppNotify": "",
        "$OOperatorPresenceStatusScripts": "",
        "$OPMCPortalStaticScripts": "",
        "$ORepeatingDynamicLayout": "",
        "$OSessionUser": "",
        "$OSurveyStaticScripts": "",
        "$OWorkformStyles": "",
        "$Ocosmoslocale": "",
        "$OmenubarInclude": "",
        "$OpxButton": "",
        "$OpxDisplayText": "",
        "$OpxDropdown": "",
        "$OpxDynamicContainer": "",
        "$OpxHarnessContent": "",
        "$OpxHeaderCell": "",
        "$OpxHidden": "",
        "$OpxIcon": "",
        "$OpxLayoutContainer": "",
        "$OpxLayoutHeader": "",
        "$OpxLink": "",
        "$OpxMenu": "",
        "$OpxNonTemplate": "",
        "$OpxSection": "",
        "$OpxTextInput": "",
        "$OpxVisible": "",
        "$OpxWorkArea": "",
        "$OpxWorkAreaContent": "",
        "$OpyDirtyCheckConfirm": "",
        "$OpyWorkFormStandardEnd": "",
        "$OpyWorkFormStandardStart": "",
        "$Opycosmoscustomstyles": "",
        "$OpzAppLauncher": "",
        "$OpzDecimalInclude": "",
        "$OpzFrameLessDCScripts": "",
        "$OpzHarnessInlineScriptsEnd": "",
        "$OpzHarnessInlineScriptsStart": "",
        "$OpzPegaCompositeGadgetScripts": "",
        "$OpzRuntimeToolsBar": "",
        "$Opzpega_ui_harnesscontext": "",
        "$Ordlincludes": "",
        "$OxmlDocumentInclude": "",
        "$OCheckbox": "",
        "$OLGBundle": "",
        "$OLayoutGroup": "",
        "$OListView_FilterPanel_Btns": "",
        "$OListView_header": "",
        "$OMicroDynamicContainer": "",
        "$OPegaSocial": "",
        "$ORepeatingGrid": "",
        "$OpxGrid": "",
        "$OpxGridBody": "",
        "$OpxGridDataCell": "",
        "$OpxGridDataRow": "",
        "$OpxGridHeaderCell": "",
        "$OpxGridHeaderRow": "",
        "$OpxMicroDynamicContainer": "",
        "$OpxTextArea": "",
        "$OpxWorkAreaHeader": "",
        "$Opycosmoscustomscripts": "",
        "$OpzLocalActionScript": "",
        "$OpzMicroDynamicContainerScripts": "",
        "$OpzTextIncludes": "",
        "$Opzcosmosuiscripts": "",
        "$Opzpega_control_attachcontent": "",
        "$OlfsInclude": "",
        "$OpxCheckbox": "",
        "pyEncodedParameters": "true",
        "pzKeepPageMessages": "false",
        "strPHarnessClass": "ESTES-OPS-YardMgmt-UIPages",
        "strPHarnessPurpose": "YardCoordinator",
        "expandRL": "false",
        "UITemplatingStatus": "Y",
        "StreamName": "pyTeamMembersWidget",
        "BaseReference": "",
        "bClientValidation": "true",
        "HeaderButtonSectionName": "-1",
        "PagesToRemove": "",
        "pzHarnessID": self.pzHarnessID,
        "inStandardsMode": "true",
    }

        logger.debug('Fetching hostler summary data')
        response = await self.async_client.post(self.details_url, data=data, params=params)
        logger.debug('Fetched hostler summary data')

        hostlers_summary = self.extract_hostler_info(response.text)
        for hostler in hostlers_summary:
            await self.upsert_hostler_summary(
                hostler_name=hostler["name"],
                moves=hostler["moves"],
                checker_id=hostler["checker_id"],
            )
        return hostlers_summary

    @staticmethod
    def filter_aggregated_payload(aggregated_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        For each hostler in the aggregated payload, filter out tasks where the door_number is
        numeric and greater than 500.
        """
        for hostler in aggregated_payload.get("hostlers", []):
            filtered_tasks = []
            for task in hostler.get("tasks", []):
                door_str = task.get("door_number", "").strip()
                try:
                    # Only keep tasks where door_number is less than or equal to 500.
                    if door_str and int(door_str) <= 500:
                        filtered_tasks.append(task)
                except ValueError:
                    # If door_number cannot be converted to an integer,
                    # you might choose to keep the task or skip it.
                    filtered_tasks.append(task)
            hostler["tasks"] = filtered_tasks
        return aggregated_payload

    @staticmethod
    def filter_out_tasks(tasks_as_dicts):
        filtered_tasks = []
        for task in tasks_as_dicts:
            door_str = task.get("door_number", "").strip()
            try:
                if int(door_str) > 500:
                    continue  # Skip this task instead of breaking out of the loop
            except ValueError:
                # If conversion fails, keep the task
                pass
            filtered_tasks.append(task)
        return filtered_tasks

    @staticmethod
    def extract_section_ids(html_content: str) -> str:
        """
        Extracts the first two containedSectionID values from the provided HTML content
        and returns a formatted string in the format:
            containedSectionID1:containedSectionID2:

        For example, if the first containedSectionID is 'GID_1739629084515' and the second is
        'GID_1739629084527', the function returns:
            'GID_1739629084515:GID_1739629084527:'
        """
        # Parse the HTML content
        tree = html.fromstring(html_content)

        # Find all elements that have a 'containedSectionID' attribute
        elements_with_id = tree.xpath("//*[@containedSectionID]")

        # Extract the containedSectionID attribute values (strip any whitespace)
        contained_ids = [elem.get("containedSectionID").strip() for elem in elements_with_id if
                         elem.get("containedSectionID")]

        # Check if we have at least two IDs and then format the string accordingly.
        if len(contained_ids) >= 2:
            sectionIDList = f"{contained_ids[0]}:{contained_ids[1]}:"
            return sectionIDList
        else:
            # If not enough IDs were found, you can handle it as needed.
            return ""

    async def fetch_workbasket_data(self):
        """
        Does the same thing as clicking the refresh button for workbasket tasks
        Then it extracts the data from the table
        :return: data from the workbasket
        """
        # Query parameters from the URL
        params = {
            "pzTransactionId": "",
            "pzFromFrame": "",
            "pzPrimaryPageName": "pyPortalHarness",
            "AJAXTrackID": "1"
        }

        # The POST data (raw) provided in the curl command.
        data = {
            "SubSectionpyGroupBasketWorkBWorkGroup": "D_PortalContextGlobal.pyActiveWorkGroup",
            "pgRepPgSubSectionpyGroupBasketWorkBPpxResults1colWidthGBL": "",
            "pgRepPgSubSectionpyGroupBasketWorkBPpxResults1colWidthGBR": "",
            "EXPANDEDSubSectionpyGroupBasketWorkB": "",
            "SubSectionpyGroupBasketWorkBBWorkGroup": "D_PortalContextGlobal.pyActiveWorkGroup",
            "pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthGBL": "",
            "pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthGBR": "",
            "pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache1": "",
            "pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache2": "",
            "pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache3": "",
            "pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache4": "",
            "pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache5": "",
            "pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache6": "",
            "pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache7": "",
            "pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache8": "",
            "pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache9": "",
            "pzuiactionzzz": f"{self.pzuiactionzzz}",
            "SectionIDList": f"{self.sectionIDList}",
            "PreActivitiesList": "",
            "sectionParam": "",
            "ActivityParams": "==",
            "$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType": "WORK",
            "$OCompositeGadget": "",
            "$OControlMenu": "",
            "$ODesktopWrapperInclude": "",
            "$ODeterminePortalTop": "",
            "$ODynamicContainerFrameLess": "",
            "$ODynamicLayout": "",
            "$ODynamicLayoutCell": "",
            "$OEvalDOMScripts_Include": "",
            "$OForm": "",
            "$OGapIdentifier": "",
            "$OGridInc": "",
            "$OHarness": "",
            "$OHarnessStaticJSEnd": "",
            "$OHarnessStaticJSStart": "",
            "$OHarnessStaticScriptsClientValidation": "",
            "$OHarnessStaticScriptsExprCal": "",
            "$OLaunchFlow": "",
            "$OMenuBar": "",
            "$OMenuBarOld": "",
            "$OMobileAppNotify": "",
            "$OOperatorPresenceStatusScripts": "",
            "$OPMCPortalStaticScripts": "",
            "$ORepeatingDynamicLayout": "",
            "$OSessionUser": "",
            "$OSurveyStaticScripts": "",
            "$OWorkformStyles": "",
            "$Ocosmoslocale": "",
            "$OmenubarInclude": "",
            "$OpxButton": "",
            "$OpxDisplayText": "",
            "$OpxDropdown": "",
            "$OpxDynamicContainer": "",
            "$OpxHarnessContent": "",
            "$OpxHeaderCell": "",
            "$OpxHidden": "",
            "$OpxIcon": "",
            "$OpxLayoutContainer": "",
            "$OpxLayoutHeader": "",
            "$OpxLink": "",
            "$OpxMenu": "",
            "$OpxNonTemplate": "",
            "$OpxSection": "",
            "$OpxTextInput": "",
            "$OpxVisible": "",
            "$OpxWorkArea": "",
            "$OpxWorkAreaContent": "",
            "$OpyDirtyCheckConfirm": "",
            "$OpyWorkFormStandardEnd": "",
            "$OpyWorkFormStandardStart": "",
            "$Opycosmoscustomstyles": "",
            "$OpzAppLauncher": "",
            "$OpzDecimalInclude": "",
            "$OpzFrameLessDCScripts": "",
            "$OpzHarnessInlineScriptsEnd": "",
            "$OpzHarnessInlineScriptsStart": "",
            "$OpzPegaCompositeGadgetScripts": "",
            "$OpzRuntimeToolsBar": "",
            "$Opzpega_ui_harnesscontext": "",
            "$Ordlincludes": "",
            "$OxmlDocumentInclude": "",
            "$OCheckbox": "",
            "$OLGBundle": "",
            "$OLayoutGroup": "",
            "$OListView_FilterPanel_Btns": "",
            "$OListView_header": "",
            "$OMicroDynamicContainer": "",
            "$OPegaSocial": "",
            "$ORepeatingGrid": "",
            "$OpxGrid": "",
            "$OpxGridBody": "",
            "$OpxGridDataCell": "",
            "$OpxGridDataRow": "",
            "$OpxGridHeaderCell": "",
            "$OpxGridHeaderRow": "",
            "$OpxMicroDynamicContainer": "",
            "$OpxTextArea": "",
            "$OpxWorkAreaHeader": "",
            "$Opycosmoscustomscripts": "",
            "$OpzLocalActionScript": "",
            "$OpzMicroDynamicContainerScripts": "",
            "$OpzTextIncludes": "",
            "$Opzcosmosuiscripts": "",
            "$Opzpega_control_attachcontent": "",
            "pyEncodedParameters": "true",
            "pzKeepPageMessages": "false",
            "strPHarnessClass": "ESTES-OPS-YardMgmt-UIPages",
            "strPHarnessPurpose": "YardCoordinator",
            "UITemplatingStatus": "Y",
            "StreamName": "pyGroupBasketWork",
            "BaseReference": "",
            "bClientValidation": "true",
            "HeaderButtonSectionName": "-1",
            "PagesToRemove": "",
            "pzHarnessID": f"{self.pzHarnessID}",
            "inStandardsMode": "true"
        }

        # logger.debug('Fetching workbasket data')
        response = await self.async_client.post(self.details_url, data=data, params=params, follow_redirects=True)
        # logger.debug(f'workbasket response code: {response.status_code}')
        # logger.debug(f'workbasket url: {self.details_url}')
        # logger.debug('Fetched workbasket data')
        # logger.debug(f'my cwd is: {os.getcwd()}')
        # with open('workbasket_data.html', 'wb') as writer:
        #     writer.write(response.content)
        return response

    async def close(self):
        logger.info("Closing async client.")
        await self.async_client.aclose()

    async def run_transfer_task(self, task_id, assigned_to):
        task_transfer = TransferTask(task_id=task_id, assigned_to=assigned_to)
        task_transfer.set_pega_data(
            details_url=self.details_url,
            pzHarnessID=self.pzHarnessID,
            async_client=self.async_client,
            csrf_token=self.csrf_token,
            fingerprint_token=self.fingerprint_token,
        )
        return await task_transfer.transfer_task()

    async def run_delete_task(self, task_id):
        task_deleter = DeleteTask(task_id=task_id)
        task_deleter.set_pega_data(
            details_url=self.details_url,
            pzHarnessID=self.pzHarnessID,
            async_client=self.async_client,
            csrf_token=self.csrf_token,
            fingerprint_token=self.fingerprint_token,
        )
        return await task_deleter.delete_task()

    async def run_create_task(
            self,
            yard_type_task,
            trailer_number,
            door_number,
            assigned_to,
            status='PENDING',
            locked=False,
            general_note='',
            priority='Normal'
    ):
        task_creator = CreateTask(
            yard_type_task=yard_type_task,
            trailer_number=trailer_number,
            door_number=door_number,
            assigned_to=assigned_to,
            status=status,
            locked=locked,
            general_note=general_note,
            priority=priority,
        )
        task_creator.set_pega_data(
            base_url=self.base_url,
            pzHarnessID=self.pzHarnessID,
            async_client=self.async_client,
            csrf_token=self.csrf_token,
            fingerprint_token=self.fingerprint_token,
        )
        created_task_data = await task_creator.create_task()
        # task_schema = TaskCreate(**created_task_data)
        # return task_schema

    async def run_delete_task(self, task_id):
        task_deleter = DeleteTask(task_id=task_id)
        task_deleter.pzHarnessID = self.pzHarnessID
        return await task_deleter.delete_task()

    async def run_transfer_task(self, task_id, assigned_to):
        task_transfer = TransferTask(task_id=task_id, assigned_to=assigned_to)
        task_transfer.pzHarnessID = self.pzHarnessID
        return await task_transfer.transfer_task()

    async def run(self):
        await self.login()
        await self.fetch_all_pega_tasks()


async def _test_create_task():
    pega = PegaTaskSessionManager()
    # await pega.run()
    await pega.login()
    await pega.run_create_task(
        yard_type_task='Bring',
        trailer_number='12345',
        door_number='99',
        # assigned_to='CLEMENTE, ELOY',
        assigned_to='',
        status='PENDING',
        locked=False,
        general_note='',
        priority='Hot',
    )


if __name__ == "__main__":
    asyncio.run(_test_create_task())
