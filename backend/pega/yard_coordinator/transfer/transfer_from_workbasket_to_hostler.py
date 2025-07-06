from backend.modules.colored_logger import setup_logger
import httpx

from backend.pega.yard_coordinator.session_manager.debug import save_html_to_file

logger = setup_logger(__name__)


class TransferFromWorkbasketToHostler:
    """
    Transfers a task from the workbasket to a hostler in Pega.
    Requires task_id and checker_id (hostler user ID) as arguments.
    All session/context must be injected via set_pega_data().
    """

    def __init__(self, task_id, checker_id, session_manager):
        self.task_id = task_id  # e.g. "T-34246622"
        self.checker_id = checker_id  # e.g. "222982"
        self.session = session_manager
        self.async_client = self.session.async_client
        self.base_url = self.session.base_url
        self.pzHarnessID = self.session.pzHarnessID
        self.details_url = self.session.details_url
        self.sectionIDList = self.session.sectionIDList
        self.debug_html = self.session.debug_html
        self.default_headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://ymg.estes-express.com",
            # Add if present in network traffic:
            "pzBFP": self.session.fingerprint_token,
            "pzCTkn": self.session.csrf_token,
        }

    async def transfer(self):
        """
        Executes the transfer and triggers reloads to update the UI.
        """
        # 1. Transfer assignment via GET
        url = (
            f"{self.base_url}"
            f"?pyActivity=TransferAssignment"
            f"&AssignmentID=ESTES-OPS-YARDMGMT-WORK%20{self.task_id}"
            f"&DestinationType=worklist"
            f"&DestinationName={self.checker_id}"
            f"&Commit=true"
            f"&PrimaryPage=pyPortalHarness"
            f"&UpdateHistory=true"
            f"&pzHarnessID={self.pzHarnessID}"
        )
        logger.debug(f'[Step 1] Transfer GET URL: {url}')
        res = await self.async_client.get(url, headers=self.default_headers)
        logger.debug(f'Transfer GET status {res.status_code}')
        if 'GOOD' not in res.text:
            follow = await self.async_client.get(res.headers["location"])
            save_html_to_file(follow.text, 2001, enabled=self.debug_html)
            if 'GOOD' not in follow.text:
                logger.error(f"Transfer GET failed: {res.status_code}")
                raise Exception(f"Transfer GET failed: {res.status_code}")
        logger.info(f"Transferred task {self.task_id} to checker_id {self.checker_id}")

        # 2. Fetch SectionIDList for reloads
        # section_id_list = await self.fetch_section_id_list()

        # 2. Reload workbasket
        reload_url = f"{self.base_url}?pzFromFrame=&pzPrimaryPageName=pyPortalHarness&AJAXTrackID=15&eventSrcSection=ESTES-OPS-YardMgmt-Work.CaseSummary"
        reload_workbasket_payload = (
            "pyActivity=ReloadSection"
            "&SubSectionpyGroupBasketWorkBWorkGroup=D_PortalContextGlobal.pyActiveWorkGroup"
            "&pgRepPgSubSectionpyGroupBasketWorkBPpxResults1colWidthGBL="
            "&pgRepPgSubSectionpyGroupBasketWorkBPpxResults1colWidthGBR="
            "&EXPANDEDSubSectionpyGroupBasketWorkB="
            "&SubSectionpyGroupBasketWorkBBWorkGroup=D_PortalContextGlobal.pyActiveWorkGroup"
            "&pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthGBL="
            "&pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthGBR="
            "&pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache1="
            "&pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache2="
            "&pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache3="
            "&pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache4="
            "&pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache5="
            "&pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache6="
            "&pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache7="
            "&pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache8="
            "&pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache9="
            f"&SectionIDList={self.sectionIDList}"
            "&PreActivitiesList="
            "&sectionParam="
            "&ActivityParams="
            "&$OCompositeGadget="
            "&$OControlMenu="
            "&$ODesktopWrapperInclude="
            "&$ODeterminePortalTop="
            "&$ODynamicContainerFrameLess="
            "&$ODynamicLayout="
            "&$ODynamicLayoutCell="
            "&$OEvalDOMScripts_Include="
            "&$OForm="
            "&$OGapIdentifier="
            "&$OGridInc="
            "&$OHarness="
            "&$OHarnessStaticJSEnd="
            "&$OHarnessStaticJSStart="
            "&$OHarnessStaticScriptsClientValidation="
            "&$OHarnessStaticScriptsExprCal="
            "&$OLaunchFlow="
            "&$OMenuBar="
            "&$OMenuBarOld="
            "&$OMobileAppNotify="
            "&$OOperatorPresenceStatusScripts="
            "&$OPMCPortalStaticScripts="
            "&$ORepeatingDynamicLayout="
            "&$OSessionUser="
            "&$OSurveyStaticScripts="
            "&$OWorkformStyles="
            "&$Ocosmoslocale="
            "&$OmenubarInclude="
            "&$OpxButton="
            "&$OpxDisplayText="
            "&$OpxDropdown="
            "&$OpxDynamicContainer="
            "&$OpxHarnessContent="
            "&$OpxHeaderCell="
            "&$OpxHidden="
            "&$OpxIcon="
            "&$OpxLayoutContainer="
            "&$OpxLayoutHeader="
            "&$OpxLink="
            "&$OpxMenu="
            "&$OpxNonTemplate="
            "&$OpxSection="
            "&$OpxTextInput="
            "&$OpxVisible="
            "&$OpxWorkArea="
            "&$OpxWorkAreaContent="
            "&$OpyDirtyCheckConfirm="
            "&$OpyWorkFormStandardEnd="
            "&$OpyWorkFormStandardStart="
            "&$Opycosmoscustomstyles="
            "&$OpzAppLauncher="
            "&$OpzDecimalInclude="
            "&$OpzFrameLessDCScripts="
            "&$OpzHarnessInlineScriptsEnd="
            "&$OpzHarnessInlineScriptsStart="
            "&$OpzPegaCompositeGadgetScripts="
            "&$OpzRuntimeToolsBar="
            "&$Opzpega_ui_harnesscontext="
            "&$Ordlincludes="
            "&$OxmlDocumentInclude="
            "&pzKeepPageMessages=false"
            "&strPHarnessClass=ESTES-OPS-YardMgmt-UIPages"
            "&strPHarnessPurpose=YardCoordinator"
            "&UITemplatingStatus=Y"
            "&StreamName=pyGroupBasketWork"
            "&BaseReference="
            "&StreamClass=Rule-HTML-Section"
            "&bClientValidation=true"
            "&PreActivity="
            "&HeaderButtonSectionName=-1"
            "&PagesToRemove="
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
            "&PreDataTransform="
        )
        res = await self.async_client.post(reload_url, data=reload_workbasket_payload, headers=self.default_headers)
        if res.status_code == 303 and "location" in res.headers:
            follow = await self.async_client.get(res.headers["location"])
            save_html_to_file(follow.text, 2002, enabled=self.debug_html)
            logger.debug(f'Reload workbasket POST status {follow.status_code}')

        # 3. Reload hostler summary widget
        reload_hostler_payload = (
            "pyActivity=ReloadSection"
            "&D_TeamMembersByWorkGroupPpxResults1colWidthGBL="
            "&D_TeamMembersByWorkGroupPpxResults1colWidthGBR="
            "&PreActivitiesList="
            "&sectionParam="
            "&ActivityParams="
            "&$OCompositeGadget="
            "&$OControlMenu="
            "&$ODesktopWrapperInclude="
            "&$ODeterminePortalTop="
            "&$ODynamicContainerFrameLess="
            "&$ODynamicLayout="
            "&$ODynamicLayoutCell="
            "&$OEvalDOMScripts_Include="
            "&$OForm="
            "&$OGapIdentifier="
            "&$OGridInc="
            "&$OHarness="
            "&$OHarnessStaticJSEnd="
            "&$OHarnessStaticJSStart="
            "&$OHarnessStaticScriptsClientValidation="
            "&$OHarnessStaticScriptsExprCal="
            "&$OLaunchFlow="
            "&$OMenuBar="
            "&$OMenuBarOld="
            "&$OMobileAppNotify="
            "&$OOperatorPresenceStatusScripts="
            "&$OPMCPortalStaticScripts="
            "&$ORepeatingDynamicLayout="
            "&$OSessionUser="
            "&$OSurveyStaticScripts="
            "&$OWorkformStyles="
            "&$Ocosmoslocale="
            "&$OmenubarInclude="
            "&$OpxButton="
            "&$OpxDisplayText="
            "&$OpxDropdown="
            "&$OpxDynamicContainer="
            "&$OpxHarnessContent="
            "&$OpxHeaderCell="
            "&$OpxHidden="
            "&$OpxIcon="
            "&$OpxLayoutContainer="
            "&$OpxLayoutHeader="
            "&$OpxLink="
            "&$OpxMenu="
            "&$OpxNonTemplate="
            "&$OpxSection="
            "&$OpxTextInput="
            "&$OpxVisible="
            "&$OpxWorkArea="
            "&$OpxWorkAreaContent="
            "&$OpyDirtyCheckConfirm="
            "&$OpyWorkFormStandardEnd="
            "&$OpyWorkFormStandardStart="
            "&$Opycosmoscustomstyles="
            "&$OpzAppLauncher="
            "&$OpzDecimalInclude="
            "&$OpzFrameLessDCScripts="
            "&$OpzHarnessInlineScriptsEnd="
            "&$OpzHarnessInlineScriptsStart="
            "&$OpzPegaCompositeGadgetScripts="
            "&$OpzRuntimeToolsBar="
            "&$Opzpega_ui_harnesscontext="
            "&$Ordlincludes="
            "&$OxmlDocumentInclude="
            "&pzKeepPageMessages=false"
            "&strPHarnessClass=ESTES-OPS-YardMgmt-UIPages"
            "&strPHarnessPurpose=YardCoordinator"
            "&expandRL=false"
            "&UITemplatingStatus=Y"
            "&StreamName=pyTeamMembersWidget"
            "&BaseReference="
            "&StreamClass=Rule-HTML-Section"
            "&bClientValidation=true"
            "&PreActivity="
            "&HeaderButtonSectionName=-1"
            "&PagesToRemove="
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
            "&PreDataTransform="
        )
        res = await self.async_client.post(reload_url, data=reload_hostler_payload, headers=self.default_headers)
        if res.status_code == 303 and "location" in res.headers:
            follow = await self.async_client.get(res.headers["location"])
            save_html_to_file(follow.text, 2003, enabled=self.session.debug_html)
            logger.debug(f'Reload hostler summary widget POST status {follow.status_code}')

        logger.info(f"Transfer from workbasket to hostler {self.checker_id} complete for task {self.task_id}.")
        return True
