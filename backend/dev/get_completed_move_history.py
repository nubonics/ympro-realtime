import pandas as pd
import io

from backend.modules.colored_logger import setup_logger

logger = setup_logger(__name__)


class GetCompletedMovesHistory:
    """
    Downloads completed moves history as an Excel file from Pega,
    and parses it to a pandas DataFrame.
    Requires all session/context injected via set_pega_data().
    """

    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.async_client = self.session_manager.async_client
        self.base_url = self.session_manager.base_url.rstrip('/')
        self.pzHarnessID = self.session_manager.pzHarnessID
        self.pzTransactionId = self.session_manager.pzTransactionId

    async def download_report(self, pzuiactionzzz, eventSrcSection="Code-Pega-List.pyReportEditorHeader"):
        """
        Triggers the report to be generated and downloaded.
        Returns: (content, content_type, headers)
        """
        url = (
            f"{self.base_url}/!DCSPA_YardCoordinator"
            f"?pzTransactionId={self.pzTransactionId}"
            f"&pzFromFrame=pyReportContentPage"
            f"&pzPrimaryPageName=pyReportContentPage"
            f"&AJAXTrackID=7"
            f"&eventSrcSection={eventSrcSection}"
        )
        payload = (
            f"pzuiactionzzz={pzuiactionzzz}"
            "&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop="
            "&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OForm="
            "&$OGridInc=&$OHarness=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart="
            "&$OHarnessStaticScriptsClientValidation=&$OLaunchFlow=&$OMenuBar="
            "&$OMenuBarOld=&$OPMCPortalStaticScripts=&$OSessionUser=&$OSurveyStaticScripts="
            "&$OWorkformStyles=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText="
            "&$OpxHarnessContainer=&$OpxHarnessContent=&$OpxLayoutContainer="
            "&$OpxLayoutHeader=&$OpxLink=&$OpxNonTemplate=&$OpxSection=&$OpxVisible="
            "&$OpyDirtyCheckConfirm=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart="
            "&$OpzDecimalInclude=&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart="
            "&$Opzpega_ui_harnesscontext=&$OxmlDocumentInclude="
            "&UITemplatingStatus=N"
            "&inStandardsMode=true"
            f"&pzHarnessID={self.pzHarnessID}"
            f"&eventSrcSection={eventSrcSection}"
        )
        response = await self.async_client.post(url, data=payload)
        logger.debug(f"Download report response status: {response.status_code}")
        assert response.status_code == 200
        return response.content, response.headers.get("content-type"), response.headers

    async def get_menu(self):
        """
        Optionally used to fetch menu/actions for the report after download (not always necessary).
        """
        url = (
            f"{self.base_url}/!DCSPA_YardCoordinator"
            f"?pzTransactionId={self.pzTransactionId}"
            f"&pzFromFrame=pyReportContentPage"
            f"&pzPrimaryPageName=pyReportContentPage"
            f"&AJAXTrackID=7"
        )
        payload = (
            "pyActivity=pzGetMenu"
            "&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop="
            "&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OForm="
            "&$OGridInc=&$OHarness=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart="
            "&$OHarnessStaticScriptsClientValidation=&$OLaunchFlow=&$OMenuBar="
            "&$OMenuBarOld=&$OPMCPortalStaticScripts=&$OSessionUser=&$OSurveyStaticScripts="
            "&$OWorkformStyles=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText="
            "&$OpxHarnessContainer=&$OpxHarnessContent=&$OpxLayoutContainer="
            "&$OpxLayoutHeader=&$OpxLink=&$OpxNonTemplate=&$OpxSection=&$OpxVisible="
            "&$OpyDirtyCheckConfirm=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart="
            "&$OpzDecimalInclude=&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart="
            "&$Opzpega_ui_harnesscontext=&$OxmlDocumentInclude="
            "&navName=pzReportActions"
            "&pzKeepPageMessages=true"
            "&removePage=true"
            "&UITemplatingStatus=Y"
            "&ContextPage=pyReportContentPage"
            "&showmenucall=true"
            "&navPageName=pyNavigation1694967022235"
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
        )
        response = await self.async_client.post(url, data=payload)
        logger.debug(f"Get menu response status: {response.status_code}")
        return response

    async def cleanup_report(self, pyPagesToRemove):
        """
        Cleans up the temporary report state in Pega after download (optional).
        """
        url = (
            f"{self.base_url}/!DCSPA_YardCoordinator"
            "?pyActivity=pyDeleteDocumentPg"
            "&pzFromFrame=pyReportContentPage"
            "&pzPrimaryPageName=pyReportContentPage"
            f"&pzHarnessID={self.pzHarnessID}"
            "&pzKeepPageMessages=true"
            "&AJAXTrackID=7"
        )
        payload = f"pyPagesToRemove={pyPagesToRemove}"
        response = await self.async_client.post(url, data=payload)
        logger.debug(f"Cleanup report response status: {response.status_code}")
        return response

    @staticmethod
    def parse_excel_to_dataframe(content):
        """
        Given a bytes Excel file, parse it to a pandas DataFrame.
        """
        try:
            df = pd.read_excel(io.BytesIO(content))
            logger.info("Successfully parsed Excel to DataFrame.")
            return df
        except Exception as e:
            logger.error(f"Failed to parse Excel: {e}")
            return None

    async def get_completed_moves_history(self, pzuiactionzzz, pyPagesToRemove):
        """
        Orchestrates the full process: download, parse, cleanup.
        Returns a pandas DataFrame.
        """
        # 1. Download Excel
        content, content_type, headers = await self.download_report(pzuiactionzzz)
        # 2. Parse to DataFrame
        df = self.parse_excel_to_dataframe(content)
        # 3. Clean up (optional)
        await self.cleanup_report(pyPagesToRemove)
        return df

    async def run(self):
        await self.get_completed_moves_history()
