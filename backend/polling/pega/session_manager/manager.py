import httpx
import asyncio
import datetime
import xxhash
import time
from os import getenv

from backend.polling.pega.create_task.create_task import CreateTask
from backend.polling.pega.delete_task import DeleteTask
from backend.polling.pega.session_manager.debug import save_html_to_file
from backend.polling.pega.session_manager.hostler_store import HostlerStore
from backend.polling.pega.session_manager.login_model import LoginError
from backend.polling.pega.session_manager.pega_parser import (
    extract_pzuiactionzzz,
    extract_section_ids,
    extract_session_data,
    extract_workbasket_tasks,
    extract_hostler_info,
    extract_hostler_view_details,
)
from backend.polling.pega.session_manager.task_store import TaskStore
from backend.polling.pega.transfer_task import TransferTask
from backend.polling.pega.session_manager.pubsub import PubSubManager


class PegaTaskSessionManager:
    def __init__(self, redis_client):
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
        self.details_url = None
        self.login_response_text = None
        self.debug_save_html = bool(getenv('PEGA_DEBUG_SAVE_HTML'))
        self.fingerprint_token = self.generate_fingerprint_token()
        self.updated_hostler_summary = False
        self.hostler_store = HostlerStore(redis_client)
        self.task_store = TaskStore(redis_client)
        self.hostler_data_memory = {}
        self.pubsub = PubSubManager(redis_client)

    @staticmethod
    def generate_fingerprint_token(seed=31):
        components = [
            {'key': 'userAgent', 'value': 'Mozilla/5.0'},
            {'key': 'language', 'value': 'en-US'},
            {'key': 'deviceMemory', 'value': 8},
            {'key': 'hardwareConcurrency', 'value': 32},
            {'key': 'timezoneOffset', 'value': 480},
            {'key': 'timezone', 'value': 'America/Los_Angeles'},
            {'key': 'localStorage', 'value': str(int(time.time()))},
            {'key': 'cpuClass', 'value': 'not available'},
            {'key': 'platform', 'value': 'Win32'},
        ]
        values = ''.join(str(component['value']) for component in components)
        fingerprint_token = '{v2}' + xxhash.xxh128(values, seed=seed).hexdigest()
        return fingerprint_token

    def should_relogin(self, max_age_hours: int = 11) -> bool:
        if self.last_login_time is None:
            return True
        elapsed = datetime.datetime.utcnow() - self.last_login_time
        return elapsed > datetime.timedelta(hours=max_age_hours)

    async def login(self):
        try:
            initial_url = "https://ymg.estes-express.com/prweb/app/default"
            initial_response = await self.async_client.get(initial_url, follow_redirects=True)
            self.base_url = str(initial_response.url)
            save_html_to_file(initial_response.content, step=1, enabled=self.debug_save_html)
            redirected_url = str(initial_response.url)
            self.redirected_url = redirected_url
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            }
            self.async_client.headers.update(headers)
            response_1 = await self.async_client.get(redirected_url)
            save_html_to_file(response_1.content, step=2, enabled=self.debug_save_html)
            self.details_url = str(response_1.url)
            captcha_url = f"{redirected_url}?pyActivity=Code-Security.pyGenerateCaptcha"
            captcha_response = await self.async_client.get(captcha_url, headers=headers, follow_redirects=True)
            save_html_to_file(captcha_response.content, step=3, enabled=self.debug_save_html)
            login_data = {
                "pzAuth": "guest",
                "UserIdentifier": getenv('PEGA_USERNAME'),
                "Password": getenv('PEGA_PASSWORD'),
                "pyActivity=Code-Security.Login": ""
            }
            login_response = await self.async_client.post(redirected_url, data=login_data, follow_redirects=True)
            save_html_to_file(login_response.content, step=4, enabled=self.debug_save_html)
            self.login_response_text = login_response.text
            self.pzuiactionzzz = extract_pzuiactionzzz(self.login_response_text)
            self.sectionIDList = extract_section_ids(self.login_response_text)
            session_tokens = extract_session_data(self.login_response_text)
            self.csrf_token = session_tokens.get("csrf_token")
            self.base_refs = session_tokens.get("base_refs", [])
            self.pzHarnessID = session_tokens.get("pzHarnessID")
            if not self.pzHarnessID:
                raise LoginError("Failed to extract session data (missing pzHarnessID)")
            self.last_login_time = datetime.datetime.utcnow()
        except Exception as e:
            raise LoginError(f"Login failed: {e}")

    async def fetch_all_pega_tasks(self):
        # Fetch workbasket data
        workbasket_html = await self.fetch_workbasket_data()
        workbasket_data = extract_workbasket_tasks(workbasket_html)
        await self.task_store.upsert_task({"id": "workbasket", "tasks": workbasket_data})
        await self.pubsub.publish("workbasket_update", workbasket_data)

        # Update hostler summary if needed
        if not self.updated_hostler_summary and self.login_response_text:
            hostlers_summary = extract_hostler_info(self.login_response_text)
            for hostler in hostlers_summary:
                await self.hostler_store.upsert_hostler(hostler)
            self.updated_hostler_summary = True
            await self.pubsub.publish("hostler_summary_update", hostlers_summary)

        # Get hostler details for each base_ref
        hostler_payloads = await asyncio.gather(
            *[self.fetch_hostler_details(base_ref) for base_ref in self.base_refs]
        )
        aggregated_payload = {"hostlers": hostler_payloads}
        await self.pubsub.publish("hostler_update", aggregated_payload)
        self.last_broadcast_payload = aggregated_payload

    async def fetch_workbasket_data(self):
        params = {
            "pzTransactionId": "",
            "pzFromFrame": "",
            "pzPrimaryPageName": "pyPortalHarness",
            "AJAXTrackID": "1"
        }
        data = {
            "SubSectionpyGroupBasketWorkBWorkGroup": "D_PortalContextGlobal.pyActiveWorkGroup",
            "pgRepPgSubSectionpyGroupBasketWorkBPpxResults1colWidthGBL": "",
            "pgRepPgSubSectionpyGroupBasketWorkBPpxResults1colWidthGBR": "",
            "pzuiactionzzz": self.pzuiactionzzz or "",
            "SectionIDList": self.sectionIDList or "",
            "pzHarnessID": self.pzHarnessID or "",
            "inStandardsMode": "true"
        }
        response = await self.async_client.post(self.details_url, data=data, params=params, follow_redirects=True)
        save_html_to_file(response.content, step=20, enabled=self.debug_save_html)
        return response.text

    async def fetch_hostler_summary_data(self):
        params = {
            "pzFromFrame": "",
            "pzPrimaryPageName": "pyPortalHarness",
            "AJAXTrackID": "1",
        }
        data = {
            "pzuiactionzzz": self.pzuiactionzzz,
            "pzHarnessID": self.pzHarnessID,
            "inStandardsMode": "true",
        }
        response = await self.async_client.post(self.details_url, data=data, params=params)
        save_html_to_file(response.content, step=21, enabled=self.debug_save_html)
        hostlers_summary = extract_hostler_info(response.text)
        for hostler in hostlers_summary:
            await self.hostler_store.upsert_hostler(hostler)
        await self.pubsub.publish("hostler_summary_update", hostlers_summary)
        return hostlers_summary

    async def fetch_hostler_details(self, base_ref):
        params = {
            "pzTransactionId": "",
            "pzFromFrame": "",
            "pzPrimaryPageName": "pyPortalHarness",
            "AJAXTrackID": "1",
            "eventSrcSection": "Data-Portal.TeamMembersGrid",
        }
        data = {
            "pyActivity": "pzRunActionWrapper",
            "rowPage": base_ref,
            "Location": "",
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
            "User-Agent": "Mozilla/5.0",
            "pzBFP": self.fingerprint_token,
            "pzCTkn": self.csrf_token or "",
        }
        response = await self.async_client.post(
            self.details_url, headers=headers, data=data, params=params, follow_redirects=True
        )
        save_html_to_file(response.content, step=30, enabled=self.debug_save_html)
        hostler_details = extract_hostler_view_details(response.text)
        hostler_name = hostler_details.get("assigned_to", "Unknown")
        tasks = hostler_details.get("tasks", [])
        for task in tasks:
            task["assigned_to"] = hostler_name
            await self.task_store.upsert_task(task)
        await self.hostler_store.upsert_hostler({
            "name": hostler_name,
            "checker_id": None,
            "moves": len(tasks),
        })
        return {
            "id": f"detail_{base_ref}",
            "name": hostler_name,
            "tasks": tasks
        }

    async def run_create_task(self, yard_type_task, trailer_number, door_number, assigned_to, status='PENDING',
                              locked=False, general_note='', priority='Normal'):
        task_creator = CreateTask(
            yard_type_task=yard_type_task,
            trailer_number=trailer_number,
            door_number=door_number,
            assigned_to=assigned_to,
            status=status,
            locked=locked,
            general_note=general_note,
            priority=priority,
            hostler_store=self.hostler_store,  # Pass HostlerStore for Redis checker lookup
        )
        task_creator.set_pega_data(
            base_url=self.base_url,
            pzHarnessID=self.pzHarnessID,
            async_client=self.async_client,
            csrf_token=self.csrf_token,
            fingerprint_token=self.fingerprint_token,
        )
        created_task_data = await task_creator.create_task()
        return created_task_data

    async def run_transfer_task(self, task_id, assigned_to, **kwargs):
        # Pass session context just like CreateTask for consistency
        task_transfer = TransferTask(
            task_id=task_id,
            assigned_to=assigned_to,
            **kwargs
        )
        task_transfer.set_pega_data(
            base_url=self.base_url,
            pzHarnessID=self.pzHarnessID,
            pzTransactionId=kwargs.get("pzTransactionId", None),  # Pass explicitly if needed
            async_client=self.async_client,
            details_url=self.details_url,
        )
        return await task_transfer.transfer()

    async def run_delete_task(self, task_id):
        task_deleter = DeleteTask(task_id=task_id)
        task_deleter.set_pega_data(
            base_url=self.base_url,
            pzHarnessID=self.pzHarnessID,
            async_client=self.async_client,
            csrf_token=self.csrf_token,
            fingerprint_token=self.fingerprint_token,
        )
        return await task_deleter.delete_task()

    async def close(self):
        await self.async_client.aclose()
