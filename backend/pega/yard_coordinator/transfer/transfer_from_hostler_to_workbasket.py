from backend.modules.colored_logger import setup_logger
import httpx
from backend.pega.yard_coordinator.session_manager.debug import save_html_to_file

logger = setup_logger(__name__)


class TransferFromHostlerToWorkbasket:
    """
    Transfers a task from a hostler (checker) to the workbasket using the Pega API's full multi-step workflow.
    All session/context must be injected via a session_manager, which provides async_client, tokens, cookies, etc.
    """

    def __init__(self, task_id, checker_id, session_manager, **kwargs):
        self.task_id = task_id  # e.g. "T-34246622"
        self.checker_id = checker_id  # e.g. "222982"
        self.session = session_manager
        self.async_client = self.session.async_client
        self.base_url = self.session.base_url
        self.pzHarnessID = self.session.pzHarnessID
        self.sectionIDList = getattr(self.session, "sectionIDList", None)
        self.fingerprint_token = self.session.fingerprint_token
        self.csrf_token = self.session.csrf_token
        self.pzuiactionzzz = getattr(self.session, "pzuiactionzzz", "")
        self.fetch_worklist_pd_key = getattr(self.session, "fetch_worklist_pd_key", "")
        self.team_members_pd_key = getattr(self.session, "team_members_pd_key", "")
        self.activity_params = getattr(self.session, "activity_params", "")
        self.row_page = kwargs.get("row_page") or getattr(self.session, "row_page", "")
        self.context_page = kwargs.get("context_page") or getattr(self.session, "context_page", "")
        self.strIndexInList = kwargs.get("strIndexInList") or getattr(self.session, "strIndexInList", "")
        self.AJAXTrackID = getattr(self.session, "AJAXTrackID", 16)
        self.pzTransactionId = getattr(self.session, "pzTransactionId", "")
        self.debug_html = getattr(self.session, "debug_html", False)

        self.default_headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://ymg.estes-express.com",
            "pzBFP": self.fingerprint_token,
            "pzCTkn": self.csrf_token,
        }

        logger.debug(f"TransferFromHostlerToWorkbasket initialized with:"
                     f"\n  task_id: {self.task_id}"
                     f"\n  checker_id: {self.checker_id}"
                     f"\n  session: {self.session!r}"
                     f"\n  async_client: {self.async_client!r}"
                     f"\n  base_url: {self.base_url!r}"
                     f"\n  pzHarnessID: {self.pzHarnessID!r}"
                     f"\n  sectionIDList: {self.sectionIDList!r}"
                     f"\n  fingerprint_token: {self.fingerprint_token!r}"
                     f"\n  csrf_token: {self.csrf_token!r}"
                     f"\n  pzuiactionzzz: {self.pzuiactionzzz!r}"
                     f"\n  fetch_worklist_pd_key: {self.fetch_worklist_pd_key!r}"
                     f"\n  team_members_pd_key: {self.team_members_pd_key!r}"
                     f"\n  activity_params: {self.activity_params!r}"
                     f"\n  row_page: {self.row_page!r}"
                     f"\n  context_page: {self.context_page!r}"
                     f"\n  strIndexInList: {self.strIndexInList!r}"
                     f"\n  AJAXTrackID: {self.AJAXTrackID!r}"
                     f"\n  pzTransactionId: {self.pzTransactionId!r}"
                     f"\n  debug_html: {self.debug_html!r}")

    async def _post_with_redirect(self, url, data, html_file_num, label):
        res = await self.async_client.post(url, data=data, headers=self.default_headers)
        save_html_to_file(res.text, html_file_num, enabled=self.debug_html)
        logger.debug(f"{label} POST status {res.status_code}")
        if res.status_code == 303 and "location" in res.headers:
            follow_url = res.headers["location"]
            if not follow_url.startswith("http"):
                follow_url = str(httpx.URL(url).join(follow_url))
            follow = await self.async_client.get(follow_url, headers=self.default_headers)
            save_html_to_file(follow.text, html_file_num + 1, enabled=self.debug_html)
            logger.debug(f"{label} POST 303-follow status {follow.status_code}")
            return follow, html_file_num + 2
        return res, html_file_num + 1

    async def _get_with_redirect(self, url, html_file_num, label):
        res = await self.async_client.get(url, headers=self.default_headers)
        save_html_to_file(res.text, html_file_num, enabled=self.debug_html)
        logger.debug(f"{label} GET status {res.status_code}")
        if res.status_code == 303 and "location" in res.headers:
            follow_url = res.headers["location"]
            if not follow_url.startswith("http"):
                follow_url = str(httpx.URL(url).join(follow_url))
            follow = await self.async_client.get(follow_url, headers=self.default_headers)
            save_html_to_file(follow.text, html_file_num + 1, enabled=self.debug_html)
            logger.debug(f"{label} GET 303-follow status {follow.status_code}")
            return follow, html_file_num + 2
        return res, html_file_num + 1

    async def step1_grid_action(self, html_file_num):
        url = (
            f"{self.base_url}?pzTransactionId={self.pzTransactionId}"
            f"&pzFromFrame=&pzPrimaryPageName=pyPortalHarness&AJAXTrackID={self.AJAXTrackID}"
            f"&eventSrcSection=Data-Portal.TeamMembersGrid"
        )
        location = (
            f"pyActivity=pzPrepareAssignment"
            f"&UITemplatingStatus=Y"
            f"&NewTaskStatus=DisplayUserWorkList"
            f"&TaskIndex="
            f"&StreamType=Rule-HTML-Section"
            f"&FieldError="
            f"&FormError="
            f"&pyCustomError="
            f"&bExcludeLegacyJS=true"
            f"&ModalSection=pzModalTemplate"
            f"&modalStyle="
            f"&IgnoreSectionSubmit=true"
            f"&bInvokedFromControl=true"
            f"&BaseReference="
            f"&isModalFlowAction=true"
            f"&bIsModal=true"
            f"&bIsOverlay=false"
            f"&StreamClass=Rule-HTML-Section"
            f"&UITemplatingScriptLoad=true"
            f"&ActionSection=pzModalTemplate"
            f"&rowPage={self.row_page}"
            f"&GridAction=true"
            f"&BaseThread=STANDARD"
            f"&pzHarnessID={self.pzHarnessID}"
        )
        payload = (
            "pyActivity=pzRunActionWrapper"
            "&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=WORK"
            f"&rowPage={self.row_page}"
            f"&Location={location}"
            f"&PagesToCopy={self.row_page}"
            f"&pzHarnessID={self.pzHarnessID}"
            "&UITemplatingStatus=N"
            "&inStandardsMode=true"
            "&eventSrcSection=Data-Portal.TeamMembersGrid"
            "&pzActivity=pzPerformGridAction"
            "&skipReturnResponse=true"
            "&pySubAction=runAct"
        )
        return await self._post_with_redirect(url, payload, html_file_num, "Step 1 (grid action)")

    async def step2_select_assignment(self, html_file_num):
        url = (
            f"{self.base_url}?pzTransactionId={self.pzTransactionId}"
            f"&pzFromFrame=&pzPrimaryPageName=pyPortalHarness&AJAXTrackID={self.AJAXTrackID}"
            "&eventSrcSection=Data-Admin-Operator-ID.WorkListGridsMain"
        )
        payload = (
            f"${self.fetch_worklist_pd_key}$ppxResults$l1$ppySelected=true"
            "&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=WORK"
            f"&pzuiactionzzz={self.pzuiactionzzz}"
            f"&BaseReference={self.row_page}"
            f"&ContextPage={self.context_page}"
            "&pzKeepPageMessages=true"
            "&pega_RLindex=1"
            "&PVClientVal=true"
            "&UITemplatingStatus=N"
            "&inStandardsMode=true"
            f"&pzHarnessID={self.pzHarnessID}"
            "&eventSrcSection=Data-Admin-Operator-ID.WorkListGridsMain"
        )
        return await self._post_with_redirect(url, payload, html_file_num, "Step 2 (select assignment)")

    async def step3_reload_worklist_grid(self, html_file_num):
        url = (
            f"{self.base_url}?pzTransactionId={self.pzTransactionId}"
            f"&pzFromFrame=&pzPrimaryPageName=pyPortalHarness&AJAXTrackID={self.AJAXTrackID}"
            "&eventSrcSection=Data-Admin-Operator-ID.WorkListGridsMain"
        )
        payload = (
            "pyActivity=ReloadSection"
            "&D_FetchWorkListAssignmentsPpxResults1colWidthGBL="
            "&D_FetchWorkListAssignmentsPpxResults1colWidthGBR="
            f"&SectionIDList={self.sectionIDList}"
            f"&${self.fetch_worklist_pd_key}$ppxResults$l1$ppySelected=true"
            f"&strIndexInList={self.strIndexInList}"
            "&PreActivitiesList="
            "&sectionParam="
            f"&ActivityParams={self.activity_params}"
            "&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=WORK"
            f"&BaseReference={self.row_page}"
            "&StreamClass=Rule-HTML-Section"
            "&partialRefresh=true"
            "&partialTrigger=editRowD_FetchWorkListAssignments.pxResults1"
            "&ReadOnly=0"
            "&bClientValidation=true"
            "&PreActivity=pzdoGridAction"
            "&HeaderButtonSectionName=-1"
            "&PagesToRemove="
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
            "&eventSrcSection=Data-Admin-Operator-ID.WorkListGridsMain"
            "&PreDataTransform="
        )
        return await self._post_with_redirect(url, payload, html_file_num, "Step 3 (reload worklist grid)")

    async def step4_select_hostler_and_submit(self, html_file_num):
        url = (
            f"{self.base_url}?pzTransactionId={self.pzTransactionId}"
            f"&pzFromFrame=&pzPrimaryPageName=pyPortalHarness&AJAXTrackID={self.AJAXTrackID}"
        )
        payload = (
            "D_FetchWorkListAssignmentsPpxResults1colWidthGBL="
            "&D_FetchWorkListAssignmentsPpxResults1colWidthGBR="
            f"&${self.team_members_pd_key}$ppxResults$l4$ppySelected=true"
            f"&${self.fetch_worklist_pd_key}$ppxResults$l1$ppySelected=true"
            f"&pzuiactionzzz={self.pzuiactionzzz}"
            f"&SectionIDList={self.sectionIDList}"
            "&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=WORK"
            "&PreActivitiesList="
            "&sectionParam="
            "&ActivityParams="
            f"&BaseReference={self.row_page}"
            "&pyEncodedParameters=true"
            "&pzKeepPageMessages=true"
            "&strPHarnessClass=ESTES-OPS-YardMgmt-UIPages"
            "&strPHarnessPurpose=YardCoordinator"
            "&UITemplatingStatus=N"
            "&StreamName=WorkListGridsMain"
            "&bClientValidation=true"
            "&HeaderButtonSectionName=-1"
            "&PagesToRemove="
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
        )
        return await self._post_with_redirect(url, payload, html_file_num, "Step 4 (select and submit)")

    async def step5_submit_modal_flow_action(self, html_file_num):
        url = (
            f"{self.base_url}?pzTransactionId={self.pzTransactionId}"
            f"&pzFromFrame=&pzPrimaryPageName=pyPortalHarness&AJAXTrackID={self.AJAXTrackID}"
        )
        payload = (
            "pyActivity=SubmitModalFlowAction"
            "&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=WORK"
            "&actionName="
            "&KeepMessages=false"
            "&ModalActionName=DisplayUserWorkList"
            "&modalSection=pzModalTemplate"
            "&bIsOverlay=false"
            f"&InterestPage={self.row_page}"
            "&HarnessType=NEW"
            "&UITemplatingStatus=Y"
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
        )
        return await self._post_with_redirect(url, payload, html_file_num, "Step 5 (submit modal flow)")

    async def transfer(self):
        """
        Runs the full transfer sequence step by step, using self's values.
        """
        html_file_num = 3000
        res, html_file_num = await self.step1_grid_action(html_file_num)
        res, html_file_num = await self.step2_select_assignment(html_file_num)
        res, html_file_num = await self.step3_reload_worklist_grid(html_file_num)
        res, html_file_num = await self.step4_select_hostler_and_submit(html_file_num)
        res, html_file_num = await self.step5_submit_modal_flow_action(html_file_num)
        logger.info(f"Transfer from hostler {self.checker_id} to workbasket complete for task {self.task_id}.")
        return True
