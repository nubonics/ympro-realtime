from backend.colored_logger import setup_logger

logger = setup_logger(__name__)


class RefreshCompletedMoves:
    """
    Refreshes the completed moves (history) report in Pega.
    Requires all context/session injected via set_pega_data().
    """

    def __init__(self):
        self.async_client = None
        self.base_url = None
        self.pzHarnessID = None
        self.pzTransactionId = None

    def set_pega_data(self, base_url, async_client, pzHarnessID, pzTransactionId):
        self.base_url = base_url.rstrip('/')
        self.async_client = async_client
        self.pzHarnessID = pzHarnessID
        self.pzTransactionId = pzTransactionId

    async def refresh_report(self, pzuiactionzzz, eventSrcSection="Code-Pega-List.pyReportEditorHeader"):
        """
        Step 1: Trigger refresh of the report.
        """
        url = (
            f"{self.base_url}/!DCSPA_YardCoordinator"
            f"?pzTransactionId={self.pzTransactionId}"
            f"&pzFromFrame=pyReportContentPage"
            f"&pzPrimaryPageName=pyReportContentPage"
            f"&AJAXTrackID=9"
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
        logger.debug(f"Refresh report response status: {response.status_code}")
        return response

    async def get_menu(self):
        """
        Step 2: Optionally fetches the menu/actions for the refreshed report.
        """
        url = (
            f"{self.base_url}/!DCSPA_YardCoordinator"
            f"?pzTransactionId={self.pzTransactionId}"
            f"&pzFromFrame=pyReportContentPage"
            f"&pzPrimaryPageName=pyReportContentPage"
            f"&AJAXTrackID=9"
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

    async def reload_visual(self, pzuiactionzzz, section_id_list):
        """
        Step 3: Reloads the visual grid after refresh.
        """
        url = (
            f"{self.base_url}/!DCSPA_YardCoordinator"
            f"?pzTransactionId={self.pzTransactionId}"
            f"&pzFromFrame=pyReportContentPage"
            f"&pzPrimaryPageName=pyReportContentPage"
            f"&AJAXTrackID=9"
        )
        payload = (
            "pyReportContentPagePpxResults1colWidthGBL=&"
            "pyReportContentPagePpxResults1colWidthGBR=&"
            "pyReportContentPagePpxResults1colWidthCache1=&"
            f"SectionIDList={section_id_list}"
            f"&pzuiactionzzz={pzuiactionzzz}"
            "&PreActivitiesList="
            "&ActivityParams=%3D"
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
            "&PreActivityContextPageList=pyReportContentPage"
            "&pzKeepPageMessages=false"
            "&strPHarnessClass=Code-Pega-List"
            "&strPHarnessPurpose=DisplayReport"
            "&BaseReference=pyReportContentPage"
            "&StreamList=pzReportDisplay%7CRule-HTML-Section%7CpyReportContentPage%7C%7C%7CY%7CSID1751148617564%7C%3A"
            "&bClientValidation=true"
            "&FormError=NONE"
            "&pyCustomError=DisplayErrors"
            "&HeaderButtonSectionName=-1"
            "&PagesToRemove="
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
        )
        response = await self.async_client.post(url, data=payload)
        logger.debug(f"Reload visual grid response status: {response.status_code}")
        return response

    async def refresh_completed_moves(self, pzuiactionzzz, section_id_list):
        """
        Orchestrates the full refresh of the completed moves report.
        """
        await self.refresh_report(pzuiactionzzz)
        await self.get_menu()
        await self.reload_visual(pzuiactionzzz, section_id_list)
        logger.info("Completed moves report refreshed.")
        return True
