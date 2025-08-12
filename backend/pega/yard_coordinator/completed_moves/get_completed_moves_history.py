import asyncio
import re
from uuid import uuid4

from backend.modules.colored_logger import setup_logger

logger = setup_logger(__name__)


class GetCompletedMovesHistory:
    """
    Async workflow for Pega 'Reports' portal navigation, using existing session manager.
    """

    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.async_client = session_manager.async_client
        self.base_url = session_manager.base_url.rstrip('/')
        self.pzHarnessID = session_manager.pzHarnessID
        self.csrf_token = session_manager.csrf_token
        self.fingerprint_token = session_manager.fingerprint_token
        self.debug_html = session_manager.debug_html
        self.dynamicContainerID = None

    async def get_homepage(self):
        """
        Step 1: GET the reports homepage and extract dynamicContainerID (tabGrpName).
        """
        url = self.session_manager.base_url
        headers = {
            **self.session_manager.get_standard_headers(),
            "Referer": self.base_url,
        }
        logger.debug(f'[Step 1] headers: {headers}')
        response = await self.async_client.get(url, headers=headers, follow_redirects=True)
        self._save_html(response.content, "homepage")
        self.dynamicContainerID = self._extract_dynamic_container_id(response.text)
        logger.info(f"Extracted dynamicContainerID: {self.dynamicContainerID}")
        return response

    @staticmethod
    def _extract_dynamic_container_id(html_text):
        match = re.search(r'"tabGrpName"\s*:\s*"([0-9a-fA-F\-]{36})"', html_text)
        if match:
            return match.group(1)
        match2 = re.search(r'tabGrpName\s*=\s*[\'"]([0-9a-fA-F\-]{36})[\'"]', html_text)
        if match2:
            return match2.group(1)
        return None

    async def post_portal_navigation(self):
        """
        Step 2: POST to the portal navigation using extracted dynamicContainerID.
        """
        contentID = str(uuid4())
        payload_template = (
            'pyActivity=%40baseclass.doUIAction&isDCSPA=true&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop='
            '&$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OForm='
            '&$OGapIdentifier=&$OGridInc=&$OHarness=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart='
            '&$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar='
            '&$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts='
            '&$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale='
            '&$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer='
            '&$OpxHarnessContent=&$OpxHeaderCell=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer='
            '&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput='
            '&$OpxVisible=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpyDirtyCheckConfirm='
            '&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles='
            '&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd='
            '&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar='
            '&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude='
            '&isSDM=true&action=display&label=Reports&className=ESTES-OPS-YardMgmt-UIPages'
            '&harnessName=Reports&contentID={contentID}&dynamicContainerID={dynamicContainerID}&SkipConflictCheck=true'
            '&readOnly=false&tabName=Reports&replaceCurrent=false&api=display'
            '&portalName=YardCoordinator&portalThreadName=STANDARD&tabIndex=1'
            f'&pzHarnessID={self.pzHarnessID}&UITemplatingStatus=Y&inStandardsMode=true&eventSrcSection=Data-Portal.PortalNavigation'
        )
        payload = payload_template.format(
            contentID=contentID,
            dynamicContainerID=self.dynamicContainerID or str(uuid4())
        )
        headers = {
            **self.session_manager.get_standard_headers(),
            "pzctkn": self.csrf_token,
            "pzbfp": self.fingerprint_token,
            "Origin": self.base_url,
        }
        url = f"{self.base_url}/!DCSPA_YardCoordinator?eventSrcSection=Data-Portal.PortalNavigation"
        response = await self.async_client.post(url, headers=headers, data=payload.encode('utf-8'), follow_redirects=True)
        self._save_html(response.content, "reports_portal")
        logger.info(f"Step 2 POST status: {response.status_code}")
        logger.debug(f'[Step 2] headers: {headers}')
        return response

    async def get_reports_shortcut(self):
        """
        Step 3: GET the actual reports page (shortcut).
        """
        headers = {
            **self.session_manager.get_standard_headers(),
        }
        url = (
            f"{self.base_url}/!DCSPA_YardCoordinator"
            "?pyActivity=%40baseclass.doUIAction"
            "&pyReportClass=ESTES-OPS-YardMgmt-Work-Task"
            "&pyShortcutHandle=YARDMANAGEMENT!S!ALL!TASKLISTBYJOCKEYWISE"
            "&action=reportDefinition"
            "&ReportAction=shortcut"
            "&pyDisplayTarget=popup"
            "&target=popup"
            "&portalThreadName=DCSPA_YardCoordinator"
            "&portalName=YardCoordinator"
            "&eventSrcSection=Data-Portal.PortalNavigation"
            f"&pzHarnessID={self.pzHarnessID}"
        )
        response = await self.async_client.get(url, headers=headers, follow_redirects=True)
        self._save_html(response.content, "reports_page")
        logger.info(f"Step 3 GET shortcut status: {response.status_code}")
        logger.debug(f'[Step 3] headers: {headers}')
        return response

    def _save_html(self, content, name):
        if self.debug_html:
            with open(f"{name}.html", "wb") as f:
                f.write(content)

    async def run(self):
        await self.get_homepage()
        await self.post_portal_navigation()
        await self.get_reports_shortcut()
