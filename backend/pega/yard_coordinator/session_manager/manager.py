import asyncio
import datetime
import json
import os
import re
import time
from os import getenv

import httpx
import xxhash
from dotenv import load_dotenv

from backend.modules.colored_logger import setup_logger
from backend.pega.yard_coordinator.completed_moves.get_completed_moves_history import GetCompletedMovesHistory
from backend.pega.yard_coordinator.completed_moves.refresh_completed_moves import RefreshCompletedMoves
from backend.pega.yard_coordinator.create_task.create_task import CreateTask
from backend.pega.yard_coordinator.session_manager.delete_task import DeleteTask
from backend.pega.yard_coordinator.session_manager.hostler_details import fetch_hostler_details
from backend.pega.yard_coordinator.session_manager.models import ReCreateHostler, LoginError
from backend.pega.yard_coordinator.open_case.open_case import OpenCase
from backend.pega.yard_coordinator.session_manager.debug import save_html_to_file
from backend.modules.hostler_store import HostlerStore
from backend.pega.yard_coordinator.session_manager.pega_parser import (
    extract_pzuiactionzzz,
    extract_section_ids,
    extract_session_data,
    extract_workbasket_tasks,
    extract_hostler_info,
)
from backend.modules.pubsub import PubSubManager
from backend.modules.task_store import TaskStore
from backend.pega.yard_coordinator.toggle_hostler_status.create_hostler import CreateHostler
from backend.pega.yard_coordinator.toggle_hostler_status.delete_hostler import DeleteHostler
from backend.pega.yard_coordinator.transfer.transfer_task import TransferTask
from backend.rules.validation import validate_and_store_tasks, delete_task_external

logger = setup_logger(__name__)
env_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
    ".env"
)
load_dotenv(dotenv_path=env_path)


class PegaTaskSessionManager:
    def __init__(self, redis_client):
        self.delete_hostler_pzuiactionzzz = None
        self.open_task_pzuiactionzzz = None
        self.pzTransactionId = None
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
        self.debug_html = getenv('PEGA_DEBUG_SAVE_HTML', '').lower() in ('1', 'true', 'yes', 'on')
        self.fingerprint_token = self.generate_fingerprint_token()
        self.updated_hostler_summary = False
        self.hostler_store = HostlerStore(redis_client)
        self.task_store = TaskStore(redis_client)
        self.hostler_data_memory = {}
        self.pubsub = PubSubManager(redis_client)
        self.deleter = DeleteTask()
        self.pyPagesToRemove = ""

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

    @staticmethod
    def extract_action_token(html_text):
        matches = re.findall(r'([A-Za-z0-9+=*/]{789,800})', html_text)
        for token in matches:
            if 789 <= len(token) <= 800:
                token = token.replace('u003d', '')
                return token
        logger.error('Unable to find pzuiactionzzz for open_task_pzuiactionzzz')
        return None

    async def login(self):
        try:
            initial_url = "https://ymg.estes-express.com/prweb/app/default"
            initial_response = await self.async_client.get(initial_url, follow_redirects=True)
            self.base_url = str(initial_response.url)
            save_html_to_file(initial_response.content, step=1, enabled=self.debug_html)
            redirected_url = str(initial_response.url)
            self.redirected_url = redirected_url
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            }
            self.async_client.headers.update(headers)
            response_1 = await self.async_client.get(redirected_url)
            save_html_to_file(response_1.content, step=2, enabled=self.debug_html)
            self.details_url = str(response_1.url)
            captcha_url = f"{redirected_url}?pyActivity=Code-Security.pyGenerateCaptcha"
            captcha_response = await self.async_client.get(captcha_url, headers=headers, follow_redirects=True)
            save_html_to_file(captcha_response.content, step=3, enabled=self.debug_html)
            login_data = {
                "pzAuth": "guest",
                "UserIdentifier": getenv('PEGA_USERNAME'),
                "Password": getenv('PEGA_PASSWORD'),
                "pyActivity=Code-Security.Login": "",
                "lockScreenID": "",
                "lockScreenPassword": "",
                "newPassword": "",
                "confirmNewPassword": "",
            }
            login_response = await self.async_client.post(redirected_url, data=login_data, follow_redirects=True)
            save_html_to_file(login_response.content, step=4, enabled=self.debug_html)
            logger.debug(f'is pega save html enabled? {self.debug_html}')
            self.login_response_text = login_response.text
            self.pzuiactionzzz = extract_pzuiactionzzz(self.login_response_text)
            logger.debug(f'self.pzuiactionzzz: {self.pzuiactionzzz}')
            self.sectionIDList = extract_section_ids(self.login_response_text)
            session_tokens = extract_session_data(self.login_response_text)
            self.csrf_token = session_tokens.get("csrf_token")
            self.base_refs = session_tokens.get("base_refs", [])
            self.pzHarnessID = session_tokens.get("pzHarnessID")
            self.pzTransactionId = session_tokens.get("pzTransactionId") or ''
            if not self.pzHarnessID:
                raise LoginError("Failed to extract session data (missing pzHarnessID)")
            self.last_login_time = datetime.datetime.utcnow()
            dashboard_response = await self.async_client.get(initial_url, follow_redirects=True)
            save_html_to_file(dashboard_response.content, step=5, enabled=self.debug_html)
            self.open_task_pzuiactionzzz = self.extract_action_token(dashboard_response.text)
            logger.debug(f'self.open_work_by_handle_pzuiactionzzz: {self.open_task_pzuiactionzzz}')
        except Exception as e:
            raise LoginError(f"Login failed: {e}")

    async def fetch_all_pega_tasks(self):
        logger.info('Fetching workbasket data...')
        workbasket_html = await self.fetch_workbasket_data()
        workbasket_data = extract_workbasket_tasks(workbasket_html)
        logger.debug('Workbasket data extracted:')
        for x in workbasket_data:
            logger.debug(x)
        try:
            valid_tasks = await validate_and_store_tasks(
                workbasket_data, self.task_store, session_manager=self
            )
        except Exception as e:
            logger.error(f"Error validating and storing workbasket tasks. {e}")
            raise
        try:
            await self.pubsub.publish("workbasket_update", [t.model_dump() for t in valid_tasks])
        except Exception as e:
            logger.error(f"Failed to publish workbasket update: {e}")
            raise e
        logger.info('Workbasket tasks fetched, validated, and stored successfully.')
        logger.debug('Checking if hostler summary needs to be updated...')
        if not self.updated_hostler_summary and self.login_response_text:
            hostlers_summary = extract_hostler_info(self.login_response_text)
            for hostler in hostlers_summary:
                await self.hostler_store.upsert_hostler(hostler)
            self.updated_hostler_summary = True
            await self.pubsub.publish("hostler_summary_update", hostlers_summary)
        logger.debug('Hostler summary updated successfully.')
        logger.debug('Fetching hostler details for each base_ref...')
        try:
            hostler_payloads = await asyncio.gather(
                *[fetch_hostler_details(base_ref=base_ref, session_manager=self) for base_ref in self.base_refs]
            )
            logger.warning(hostler_payloads)
        except Exception as e:
            logger.error(f"Error fetching hostler payloads: {e}")
            raise e
        aggregated_payload = {"hostlers": hostler_payloads}
        logger.debug(f'Aggregated hostler payload:\n')
        for x in aggregated_payload:
            logger.debug(json.dumps(x))

        await self.pubsub.publish("hostler_update", aggregated_payload)
        self.last_broadcast_payload = aggregated_payload
        logger.info('Hostler details fetched and broadcasted successfully.')

    async def fetch_workbasket_data(self):
        params = {
            "pzTransactionId": self.pzTransactionId or "",
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
        save_html_to_file(response.content, step=20, enabled=self.debug_html)
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
        save_html_to_file(response.content, step=21, enabled=self.debug_html)
        hostlers_summary = extract_hostler_info(response.text)
        for hostler in hostlers_summary:
            await self.hostler_store.upsert_hostler(hostler)
        await self.pubsub.publish("hostler_summary_update", hostlers_summary)
        return hostlers_summary

    def get_standard_headers(self):
        return {
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

    def get_standard_params(self):
        return {
            "pzTransactionId": self.pzTransactionId or "",
            "pzFromFrame": "",
            "pzPrimaryPageName": "pyPortalHarness",
            "AJAXTrackID": "1",
            "eventSrcSection": "Data-Portal.TeamMembersGrid",
        }

    def _get_first_page_payload(self, base_ref):
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

        return {
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

    @staticmethod
    def get_pagelist_property(hostler_details):
        for task in hostler_details.get("tasks", []):
            if "pagelist_property" in task:
                return task["pagelist_property"]

    async def run_create_task(self, yard_task_type, trailer_number, door, assigned_to, status='PENDING',
                              locked=False, general_note='', priority='Normal'):
        task_creator = CreateTask(
            yard_task_type=yard_task_type,
            trailer_number=trailer_number,
            door=door,
            assigned_to=assigned_to,
            status=status,
            locked=locked,
            general_note=general_note,
            priority=priority,
            hostler_store=self.hostler_store,
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

    async def run_delete_task(self, case_id: str):
        # Delete the externally
        await self.deleter.delete_task(case_id=case_id)
        # Delete the task from the local store
        await delete_task_external(case_id=case_id, task_store=self.task_store, session_manager=self)

    async def run_transfer_task(self, case_id, assigned_to, target, redis):
        """
        Handles transfer logic for hostler->workbasket, workbasket->hostler, hostler->hostler.
        Args:
            case_id: The task/case id
            assigned_to: The current assignment (hostler id or None for workbasket)
            target: The desired assignment (hostler id or None for workbasket)
            redis: Redis client
        Returns:
            The created task dictionary
        """
        task_transfer = TransferTask(
            case_id=case_id,
            assigned_to=assigned_to,
            target=target,
            session_manager=self
        )
        return await task_transfer.transfer(redis=redis)

    async def close(self):
        await self.async_client.aclose()

    async def get_completed_hostler_history(self):
        await GetCompletedMovesHistory(session_manager=self).run()

    async def refresh_all_hostlers_history(self):
        await RefreshCompletedMoves(session_manager=self).run()

    @staticmethod
    async def open_case(case_id, session_manager):
        """
        Opens a case by its ID.
        Args:
            case_id: The ID of the case to open.
            session_manager: An instance of OpenCase to manage the session.
        Returns:
            The response from opening the case.
        """
        case = OpenCase(
            case_id=case_id,
            session_manager=session_manager,
        )

        return await case.run()

    @staticmethod
    async def delete_hostler(hostler: "ReCreateHostler", session_manager: "PegaTaskSessionManager"):
        """
        Deletes a hostler.
        """
        await DeleteHostler(session_manager=session_manager, hostler=hostler).run()

    async def create_hostler(self, hostler: "ReCreateHostler", session_manager: "PegaTaskSessionManager"):
        """
        Creates a hostler.
        """
        await CreateHostler(session_manager=session_manager, hostler=hostler).run(self.delete_hostler_pzuiactionzzz)

    async def recreate_hostler(self, hostler: "ReCreateHostler", session_manager: "PegaTaskSessionManager"):
        """
        Recreates a hostler.
        """
        self.delete_hostler_pzuiactionzzz = await self.delete_hostler(hostler=hostler, session_manager=session_manager)
        await self.create_hostler(hostler=hostler, session_manager=session_manager)

        return {"status": "ok"}
