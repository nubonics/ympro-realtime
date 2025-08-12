import httpx
import http.cookies
from lxml import html as lxml_html

from backend.modules.colored_logger import setup_logger
from backend.pega.yard_coordinator.session_manager.hostler_details import fetch_hostler_details
from backend.pega.yard_coordinator.session_manager.pega_parser import extract_grid_action_fields, get_row_page

logger = setup_logger(__name__)

class TransferFromHostlerToWorkbasket:
    """
    Transfers a task from a hostler (checker) to the workbasket using the Pega API's full multi-step workflow.
    All session/context must be injected via a session_manager, which provides async_client, tokens, cookies, etc.
    """

    def __init__(self, case_id, checker_id, session_manager, **kwargs):
        self.selected_row_id = None
        self.pyPropertyTarget = None
        self.base_ref_step2 = None
        self.context_page = None
        self.pzuiactionzzz = None

        self.case_id = case_id  # e.g. "T-34246622"
        self.checker_id = checker_id  # e.g. "222982"
        self.session = session_manager
        self.async_client = self.session.async_client
        self.base_url = self.session.base_url
        self.pzHarnessID = self.session.pzHarnessID
        self.fingerprint_token = self.session.fingerprint_token
        self.csrf_token = self.session.csrf_token
        self.AJAXTrackID = "1"
        self.pzTransactionId = getattr(self.session, "pzTransactionId", "")
        self.debug_html = getattr(self.session, "debug_html", False)
        self.pzTransactionId = self.session.pzTransactionId

        # --- Always use kwargs, which should be per-task/store context ---
        self.base_ref = kwargs.get("base_ref", "")
        self.section_id_list = kwargs.get("section_id_list", "")
        self.fetch_worklist_pd_key = kwargs.get("fetch_worklist_pd_key", "")
        self.team_members_pd_key = kwargs.get("team_members_pd_key", "")
        self.activity_params = kwargs.get("activity_params", "")
        self.row_page = kwargs.get("row_page", "")
        self.strIndexInList = kwargs.get("strIndexInList", "")

        # You should set these cookies manually (get from browser or session manager)
        self.pega_cookies = kwargs.get("pega_cookies", {
            # Example format; populate with real values
            "Pega-Perf": "itkn=13&start",
            "Pega-RULES": "",
            "JSESSIONID": "",
            "NSC_MC-ZBSE-QSE-TTM": "",
        })

        self.default_headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "DNT": "1",
            "Host": "ymg.estes-express.com",
            "Origin": "https://ymg.estes-express.com",
            "Pragma": "no-cache",
            "Referer": "https://ymg.estes-express.com/prweb/app/YardMgmt/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!STANDARD?pzPostData=-1084884441",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "pzBFP": self.fingerprint_token,
            "pzCTkn": self.csrf_token,
        }

        logger.debug(f"TransferFromHostlerToWorkbasket initialized with:"
                     f"\n  case_id: {self.case_id}"
                     f"\n  checker_id: {self.checker_id}"
                     f"\n  session: {self.session!r}"
                     f"\n  async_client: {self.async_client!r}"
                     f"\n  base_url: {self.base_url!r}"
                     f"\n  pzHarnessID: {self.pzHarnessID!r}"
                     f"\n  section_id_list: {self.section_id_list!r}"
                     f"\n  fingerprint_token: {self.fingerprint_token!r}"
                     f"\n  csrf_token: {self.csrf_token!r}"
                     f"\n  fetch_worklist_pd_key: {self.fetch_worklist_pd_key!r}"
                     f"\n  team_members_pd_key: {self.team_members_pd_key!r}"
                     f"\n  activity_params: {self.activity_params!r}"
                     f"\n  row_page: {self.row_page!r}"
                     f"\n  context_page: {self.context_page!r}"
                     f"\n  strIndexInList: {self.strIndexInList!r}"
                     f"\n  AJAXTrackID: {self.AJAXTrackID!r}"
                     f"\n  pzTransactionId: {self.pzTransactionId!r}"
                     f"\n  debug_html: {self.debug_html!r}")

    @staticmethod
    def _cookie_header_from_dict(cookies: dict) -> str:
        # Helper: convert cookies dict to a single Cookie header string
        return "; ".join(f"{k}={v}" for k, v in cookies.items() if v)

    def _update_cookies_from_response(self, response):
        # Update self.pega_cookies from Set-Cookie headers in response
        set_cookie_headers = response.headers.get_list('set-cookie')
        for header in set_cookie_headers:
            c = http.cookies.SimpleCookie()
            c.load(header)
            for key in c:
                self.pega_cookies[key] = c[key].value

    @staticmethod
    def _is_login_page(html_text):
        return (
            "login" in html_text.lower() or
            "sign in" in html_text.lower() or
            "username" in html_text.lower() or
            "password" in html_text.lower()
        )

    async def _post_expect_200(self, url, data, html_file_num, label):
        headers = self.default_headers.copy()
        if self.pega_cookies:
            headers["Cookie"] = self._cookie_header_from_dict(self.pega_cookies)
        res = await self.async_client.post(url, data=data, headers=headers, follow_redirects=False)
        logger.debug(f'{label} POST status {res.status_code} for {url}')
        with open(f'{html_file_num}.html', 'w') as writer:
            writer.write(res.text)
        # Update cookies after every response!
        self._update_cookies_from_response(res)
        # save_html_to_file(res.text, html_file_num, enabled=self.debug_html)
        if res.status_code != 200:
            logger.error(f"{label} failed: Expected HTTP 200, got {res.status_code}. Response headers: {res.headers}")
            raise httpx.HTTPStatusError(
                f"{label} failed: Expected HTTP 200, got {res.status_code}.",
                request=res.request,
                response=res
            )
        if self._is_login_page(res.text):
            logger.error(f"{label} failed: Received login page HTML; authentication/session may be expired or invalid.")
            raise httpx.HTTPStatusError(
                f"{label} failed: Received login page HTML.",
                request=res.request,
                response=res
            )
        return res, html_file_num + 1

    async def step1_grid_action(self, html_file_num):
        task_data = await self.session.task_store.get_task(self.case_id)
        self.base_ref = task_data['base_ref']
        self.row_page = get_row_page(self.base_ref)

        details = await fetch_hostler_details(self.session, self.base_ref, step1_grid_action=True)
        html_text = details.get("raw_html", "")
        tree = lxml_html.fromstring(html_text)
        found_row_id = None

        for tr in tree.xpath("//tr[contains(@class, 'cellCont')]"):
            attrs = tr.attrib
            oa_args = attrs.get("OAArgs") or attrs.get("oaargs") or ""
            if self.case_id in oa_args:
                found_row_id = attrs.get("id")
                logger.debug(f"Found grid row id for case_id {self.case_id}: {found_row_id}")
                break

        if not found_row_id:
            logger.error("No matching <tr> found. Dumping all <tr> OAArgs and ids for debug:")
            for tr in tree.xpath("//tr[contains(@class, 'cellCont')]"):
                logger.error(f"OAArgs: {tr.attrib.get('OAArgs') or tr.attrib.get('oaargs')}, id: {tr.attrib.get('id')}")
            raise RuntimeError(f"Could not find grid row id for task {self.case_id} in hostler grid.")

        self.selected_row_id = found_row_id
        logger.debug(f"[ Step 1 grid_action ] selected row id : {self.selected_row_id}")

        grid_fields = extract_grid_action_fields(html_text)
        self.pyPropertyTarget = grid_fields.get("pyPropertyTarget", "")
        self.base_ref_step2 = grid_fields.get("base_ref", "")
        self.context_page = grid_fields.get("context_page", "")
        self.pzuiactionzzz = grid_fields.get("pzuiactionzzz", "")
        self.pzHarnessID = grid_fields.get("pzHarnessID") or self.session.pzHarnessID
        self.row_page = grid_fields.get("row_page", "")

        '''
        self.pzHarnessID = grid_fields.get("pzHarnessID", "")
        if not self.pzHarnessID:
            # fallback to task_data or session value
            self.pzHarnessID = task_data.get("pzHarnessID") or self.pzHarnessID or self.session.pzHarnessID
        '''

        logger.debug(f"Extracted grid fields for step2_select_assignment: {grid_fields}")

    async def step2_select_assignment(self, html_file_num):
        url = (
            f"{self.base_url.replace('STANDARD', 'DCSPA_YardCoordinator')}?pzTransactionId={self.pzTransactionId}"
            f"&pzFromFrame=&pzPrimaryPageName=pyPortalHarness&AJAXTrackID={self.AJAXTrackID}"
            "&eventSrcSection=Data-Admin-Operator-ID.WorkListGridsMain"
        )

        o_keys = [
            "$OCompositeGadget", "$OControlMenu", "$ODesktopWrapperInclude", "$ODeterminePortalTop",
            "$ODynamicContainerFrameLess", "$ODynamicLayout", "$ODynamicLayoutCell", "$OEvalDOMScripts_Include",
            "$OGapIdentifier", "$OHarnessStaticJSEnd", "$OHarnessStaticJSStart", "$OHarnessStaticScriptsClientValidation",
            "$OHarnessStaticScriptsExprCal", "$OLaunchFlow", "$OMenuBar", "$OMenuBarOld", "$OMobileAppNotify",
            "$OOperatorPresenceStatusScripts", "$OPMCPortalStaticScripts", "$ORepeatingDynamicLayout", "$OSessionUser",
            "$OSurveyStaticScripts", "$OWorkformStyles", "$Ocosmoslocale", "$OmenubarInclude", "$OpxButton",
            "$OpxDisplayText", "$OpxDropdown", "$OpxDynamicContainer", "$OpxHidden", "$OpxIcon",
            "$OpxLayoutContainer", "$OpxLayoutHeader", "$OpxLink", "$OpxMenu", "$OpxNonTemplate", "$OpxSection",
            "$OpxTextInput", "$OpxVisible", "$OpyWorkFormStandardEnd", "$OpyWorkFormStandardStart", "$Opycosmoscustomstyles",
            "$OpzAppLauncher", "$OpzDecimalInclude", "$OpzFrameLessDCScripts", "$OpzHarnessInlineScriptsEnd",
            "$OpzHarnessInlineScriptsStart", "$OpzPegaCompositeGadgetScripts", "$OpzRuntimeToolsBar", "$Opzpega_ui_harnesscontext",
            "$Ordlincludes", "$OxmlDocumentInclude", "$OForm", "$OGridInc", "$OHarness", "$OpxHarnessContent",
            "$OpxHeaderCell", "$OpxWorkArea", "$OpxWorkAreaContent", "$OpyDirtyCheckConfirm", "$OCheckbox",
            "$OLGBundle", "$OLayoutGroup", "$OMicroDynamicContainer", "$ONewActionSection", "$OPegaSocial",
            "$OpxMicroDynamicContainer", "$OpxTextArea", "$OpxWorkAreaHeader", "$Opycosmoscustomscripts",
            "$OpzMicroDynamicContainerScripts", "$OpzTextIncludes", "$Opzcosmosuiscripts", "$Opzpega_control_attachcontent",
            "$OpxAutoComplete", "$OpxRadioButtons", "$OpzAutoCompleteAGIncludes", "$OpzRadiogroupIncludes"
        ]

        payload_parts = [
            f"{self.selected_row_id or ''}$ppySelected=true"
        ] + [
            f"{key}=" for key in o_keys
        ] + [
            f"pzuiactionzzz={self.pzuiactionzzz or ''}",
            f"pyPropertyTarget={self.pyPropertyTarget or ''}",
            "updateDOM=true",
            f"BaseReference={self.base_ref_step2 or ''}",
            f"ContextPage={self.context_page or ''}",
            "pzKeepPageMessages=true",
            "pega_RLindex=1",
            "PVClientVal=true",
            "UITemplatingStatus=N",
            "inStandardsMode=true",
            f"pzHarnessID={self.pzHarnessID or ''}",
            "eventSrcSection=Data-Admin-Operator-ID.WorkListGridsMain"
        ]
        payload = "&".join(payload_parts)
        logger.debug(f'[Step 2] payload: {payload}')

        return await self._post_expect_200(url, payload, html_file_num, "Step 2 (select assignment)")

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
            f"&SectionIDList={self.section_id_list or ''}"
            f"&${self.fetch_worklist_pd_key or ''}$ppxResults$l1$ppySelected=true"
            f"&strIndexInList={self.strIndexInList or ''}"
            "&PreActivitiesList="
            "&sectionParam="
            f"&ActivityParams={self.activity_params or ''}"
            "&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=WORK"
            f"&BaseReference={self.row_page or ''}"
            "&StreamClass=Rule-HTML-Section"
            "&partialRefresh=true"
            "&partialTrigger=editRowD_FetchWorkListAssignments.pxResults1"
            "&ReadOnly=0"
            "&bClientValidation=true"
            "&PreActivity=pzdoGridAction"
            "&HeaderButtonSectionName=-1"
            "&PagesToRemove="
            f"&pzHarnessID={self.pzHarnessID or ''}"
            "&inStandardsMode=true"
            "&eventSrcSection=Data-Admin-Operator-ID.WorkListGridsMain"
            "&PreDataTransform="
        )
        return await self._post_expect_200(url, payload, html_file_num, "Step 3 (reload worklist grid)")

    async def step4_select_hostler_and_submit(self, html_file_num):
        url = (
            f"{self.base_url}?pzTransactionId={self.pzTransactionId}"
            f"&pzFromFrame=&pzPrimaryPageName=pyPortalHarness&AJAXTrackID={self.AJAXTrackID}"
        )
        payload = (
            "D_FetchWorkListAssignmentsPpxResults1colWidthGBL="
            "&D_FetchWorkListAssignmentsPpxResults1colWidthGBR="
            f"&${self.team_members_pd_key or ''}$ppxResults$l4$ppySelected=true"
            f"&${self.fetch_worklist_pd_key or ''}$ppxResults$l1$ppySelected=true"
            f"&pzuiactionzzz={self.pzuiactionzzz or ''}"
            f"&SectionIDList={self.section_id_list or ''}"
            "&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=WORK"
            "&PreActivitiesList="
            "&sectionParam="
            "&ActivityParams="
            f"&BaseReference={self.row_page or ''}"
            "&pyEncodedParameters=true"
            "&pzKeepPageMessages=true"
            "&strPHarnessClass=ESTES-OPS-YardMgmt-UIPages"
            "&strPHarnessPurpose=YardCoordinator"
            "&UITemplatingStatus=N"
            "&StreamName=WorkListGridsMain"
            "&bClientValidation=true"
            "&HeaderButtonSectionName=-1"
            "&PagesToRemove="
            f"&pzHarnessID={self.pzHarnessID or ''}"
            "&inStandardsMode=true"
        )
        return await self._post_expect_200(url, payload, html_file_num, "Step 4 (select and submit)")

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
            f"&InterestPage={self.row_page or ''}"
            "&HarnessType=NEW"
            "&UITemplatingStatus=Y"
            f"&pzHarnessID={self.pzHarnessID or ''}"
            "&inStandardsMode=true"
        )
        return await self._post_expect_200(url, payload, html_file_num, "Step 5 (submit modal flow)")

    async def transfer(self):
        html_file_num = 3000
        await self.step1_grid_action(html_file_num=html_file_num)
        await self.step2_select_assignment(html_file_num+2)
        await self.step3_reload_worklist_grid(html_file_num+3)
        await self.step4_select_hostler_and_submit(html_file_num+4)
        await self.step5_submit_modal_flow_action(html_file_num+5)
        logger.info(f"Transfer from hostler {self.checker_id} to workbasket complete for task {self.case_id}.")
        return True
