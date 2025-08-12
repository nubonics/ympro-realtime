from backend.modules.colored_logger import setup_logger

logger = setup_logger(__name__)


class RefreshCompletedMoves:
    """
    Refreshes the completed moves (history) report in Pega.
    Requires all context/session injected via set_pega_data().
    """

    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.async_client = self.session_manager.async_client
        self.base_url = self.session_manager.base_url.rstrip('/')
        self.pzHarnessID = self.session_manager.pzHarnessID
        self.pzTransactionId = self.session_manager.pzTransactionId
        self.pzuiactionzzz = self.session_manager.pzuiactionzzz
        self.section_id_list = self.session_manager.section_id_list

    def set_pega_data(self, pzuiactionzzz, section_id_list):
        self.pzuiactionzzz = pzuiactionzzz
        self.section_id_list = section_id_list

    async def refresh_report(self, eventSrcSection="Code-Pega-List.pyReportEditorHeader"):
        url = (
            f"{self.base_url}/!DCSPA_YardCoordinator"
            f"?pzTransactionId={self.pzTransactionId}"
            f"&pzFromFrame=pyReportContentPage"
            f"&pzPrimaryPageName=pyReportContentPage"
            f"&AJAXTrackID=9"
            f"&eventSrcSection={eventSrcSection}"
        )
        payload = (
            f"pzuiactionzzz={self.pzuiactionzzz}"
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

    async def reload_visual(self):
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
            f"SectionIDList={self.section_id_list}"
            f"&pzuiactionzzz={self.pzuiactionzzz}"
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

    async def refresh_completed_moves(self):
        await self.refresh_report()
        await self.get_menu()
        await self.reload_visual()
        logger.info("Completed moves report refreshed.")
        return True

    async def run(self):
        if self.pzuiactionzzz is None or self.section_id_list is None:
            raise ValueError("pzuiactionzzz and section_id_list must be set with set_pega_data() before calling run().")
        return await self.refresh_completed_moves()
