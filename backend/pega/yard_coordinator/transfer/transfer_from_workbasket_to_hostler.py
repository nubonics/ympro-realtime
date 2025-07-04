from backend.modules.colored_logger import setup_logger
logger = setup_logger(__name__)


class TransferFromWorkbasketToHostler:
    """
    Transfers a task from the workbasket to a hostler in Pega.
    Requires task_id and checker_id (hostler user ID) as arguments.
    All session/context must be injected via set_pega_data().
    """

    def __init__(self, task_id, checker_id):
        self.task_id = task_id  # e.g. "T-34246622"
        self.checker_id = checker_id  # e.g. "222982"
        self.async_client = None
        self.base_url = None
        self.pzHarnessID = None
        self.details_url = None

    def set_pega_data(self, base_url, pzHarnessID, async_client, details_url=None):
        """
        Injects all session/context values required for the transfer.
        """
        self.base_url = base_url.rstrip('/')
        self.pzHarnessID = pzHarnessID
        self.async_client = async_client
        self.details_url = details_url or self.base_url

    async def transfer(self):
        """
        Executes the transfer and triggers reloads to update the UI.
        """
        # 1. Transfer assignment via GET
        # Build the URL with all required query params
        url = (
            f"{self.base_url.replace('!STANDARD', '!STANDARD')}"
            f"?pyActivity=TransferAssignment"
            f"&AssignmentID=ESTES-OPS-YARDMGMT-WORK%20{self.task_id}"
            f"&DestinationType=worklist"
            f"&DestinationName={self.checker_id}"
            f"&Commit=true"
            f"&PrimaryPage=pyPortalHarness"
            f"&UpdateHistory=true"
            f"&pzHarnessID={self.pzHarnessID}"
        )

        response = await self.async_client.get(url)
        logger.debug(f'Transfer GET status {response.status_code}')
        assert response.status_code == 200
        logger.info(f"Transferred task {self.task_id} to checker_id {self.checker_id}")

        # 2. Reload hostler summary widget (optional, but matches UI refresh)
        reload_url = f"{self.base_url.replace('!STANDARD', '!STANDARD')}?pzTransactionId=&pzFromFrame=&pzPrimaryPageName=pyPortalHarness&AJAXTrackID=5"
        reload_payload = (
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
        response = await self.async_client.post(reload_url, data=reload_payload)
        logger.debug(f'Reload hostler summary widget POST status {response.status_code}')

        # 3. Reload workbasket (optional, but matches UI refresh)
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
            "&SectionIDList="
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
        response = await self.async_client.post(reload_url, data=reload_workbasket_payload)
        logger.debug(f'Reload workbasket POST status {response.status_code}')

        logger.info(f"Transfer from workbasket to hostler {self.checker_id} complete for task {self.task_id}.")
        return True
