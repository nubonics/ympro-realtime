from backend.pega.yard_coordinator.create_task.create_task_parser import extract_pzuiactionzzz, get_pzTransactionId, \
    get_PD_pzRenderFeedContext, get_PD_pzFeedParams
from backend.pega.yard_coordinator.session_manager.debug import save_html_to_file
from backend.modules.colored_logger import setup_logger
import time
from uuid import uuid4
logger = setup_logger(__name__)


class CreateTask:
    def __init__(
        self,
        yard_task_type,
        trailer_number,
        door,
        assigned_to,
        status='PENDING',
        locked=False,
        general_note=str(),
        priority='Normal',
        hostler_store=None,  # Pass HostlerStore instance!
    ):
        self.async_client = None
        self.pzHarnessID = None
        self.base_url = None
        self.pega_base_url_to_create_task = None
        self.csrf_token = None
        self.fingerprint_token = None
        self.assigned_to_checker_id = None
        self.async_counter = 1
        self.yard_task_type = self.format_yard_task_type(yard_task_type=yard_task_type)
        self.trailer_number = trailer_number
        self.door = door
        self.assigned_to = assigned_to
        self.status = status
        self.locked = locked
        self.general_note = general_note
        self.priority = priority
        self.pzuiactionzzz = None
        self.pzTransactionId_1 = None
        self.pzTransactionId_2 = None
        self.PD_pzFeedParams = None
        self.PD_pzRenderFeedContext = None
        self.hostler_store = hostler_store

    async def set_checker_id(self):
        if self.assigned_to and self.assigned_to.lower() != "workbasket" and self.hostler_store:
            self.assigned_to_checker_id = await self.hostler_store.lookup_checker_id(self.assigned_to)
        else:
            self.assigned_to_checker_id = ""

    @staticmethod
    def format_yard_task_type(yard_task_type):
        types = {'bring': 'BringToDock', 'pull': 'RemoveFromDock', 'hook': 'Hook Trailer'}
        return types.get(yard_task_type.lower(), yard_task_type)

    def set_pega_data(self, base_url, pzHarnessID, async_client, csrf_token, fingerprint_token):
        self.base_url = base_url
        self.pzHarnessID = pzHarnessID
        base_url_str = str(self.base_url)
        self.pega_base_url_to_create_task = f"{base_url_str.replace('STANDARD', 'DCSPA_YardCoordinator')}"
        self.async_client = async_client
        self.csrf_token = csrf_token
        self.fingerprint_token = fingerprint_token
        headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "DNT": "1",
            "Origin": "https://ymg.estes-express.com",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "X-Requested-With": "XMLHttpRequest",
        }
        self.async_client.headers.update(headers)

    async def create_task(self):
        await self.set_checker_id()
        await self.step1()
        await self.step3()
        await self.step5()
        await self.step2()
        await self.step6()
        await self.step4()

    async def step1(self):
        logger.debug('Create Task - Starting Step # 1')
        # url = (
        #     "https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/"
        #     "!DCSPA_YardCoordinator?eventSrcSection=Data-Portal.PortalNavigation"
        # )
        # url = url.replace('STANDARD', 'DCSPA_YardCoordinator?')
        # Build the raw form data string as provided (ensure the proper URL encoding is preserved)
        params = {
            "eventSrcSection": "Data-Portal.PortalNavigation"
        }
        data = (
            "pyActivity=%40baseclass.doUIAction"
            "&isDCSPA=true"
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
            "&$OLGBundle="
            "&$OLayoutGroup="
            "&$OMicroDynamicContainer="
            "&$ONewActionSection="
            "&$OPegaSocial="
            "&$OpxMicroDynamicContainer="
            "&$OpxTextArea="
            "&$OpxWorkAreaHeader="
            "&$Opycosmoscustomscripts="
            "&$OpzMicroDynamicContainerScripts="
            "&$OpzTextIncludes="
            "&$Opzcosmosuiscripts="
            "&$Opzpega_control_attachcontent="
            "&$OpxAutoComplete="
            "&$OpxRadioButtons="
            "&$OpzAutoCompleteAGIncludes="
            "&$OpzRadiogroupIncludes="
            "&$OCheckbox="
            "&$OListView_FilterPanel_Btns="
            "&$OListView_header="
            "&$ORepeatingGrid="
            "&$OpxGrid="
            "&$OpxGridBody="
            "&$OpxGridDataCell="
            "&$OpxGridDataRow="
            "&$OpxGridHeaderCell="
            "&$OpxGridHeaderRow="
            "&$OpzLocalActionScript="
            "&isSDM=true"
            "&action=createNewWork"
            "&flowClass=ESTES-OPS-YardMgmt-Work-Task"
            "&className=ESTES-OPS-YardMgmt-Work-Task"
            "&flowName=pyStartCase"
            "&SkipConflictCheck=false"
            "&api=createNewWork"
            f"&contentID={uuid4()}"
            f"&dynamicContainerID={uuid4()}"
            "&portalName=YardCoordinator"
            "&portalThreadName=STANDARD"
            "&tabIndex=1"
            f"&pzHarnessID={self.pzHarnessID}"
            "&UITemplatingStatus=Y"
            "&inStandardsMode=true"
            "&eventSrcSection=Data-Portal.PortalNavigation"
        )
        response = await self.async_client.post(
            url=self.pega_base_url_to_create_task,
            data=data,
            params=params,
            follow_redirects=True
        )
        save_html_to_file(content=response.content, step=1)
        logger.debug(f'step 1 response code: {response.status_code}')
        logger.debug(f'step # 1 response url: {response.url}')
        assert response.status_code == 200 or 303

        content = response.content
        self.pzuiactionzzz = extract_pzuiactionzzz(html_content=content)
        self.pzTransactionId_1 = get_pzTransactionId(html_content=content)
        self.PD_pzRenderFeedContext = get_PD_pzRenderFeedContext(html_content=content)
        self.PD_pzFeedParams = get_PD_pzFeedParams(html_content=content)
        del content

        logger.debug(f'self.pzuiactionzzz: {self.pzuiactionzzz}')
        logger.debug(f'self.pzTransactionId: {self.pzTransactionId_1}')
        logger.debug(f'self.PD_pzRenderFeedContext: {self.PD_pzRenderFeedContext}')
        logger.debug(f'self.PD_pzFeedParams: {self.PD_pzFeedParams}')

        logger.debug('Create Task - Ending Step # 1')

        return response.text

    async def step2(self):
        logger.debug('Create Task - Starting Step # 2')
        params = {
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "pzTransactionId": self.pzTransactionId_1,
            "eventSrcSection": "Data-Portal-PortalNavigation"
        }
        data = (
            f"$PpyWorkPage$pMetaData$pTaskType={self.yard_task_type}"
            f"&pzuiactionzzz={self.pzuiactionzzz}"
            "&PreActivitiesList="
            "&sectionParam="
            "&ActivityParams=%3D"
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
            "&$OLGBundle="
            "&$OLayoutGroup="
            "&$OMicroDynamicContainer="
            "&$ONewActionSection="
            "&$OPegaSocial="
            "&$OpxMicroDynamicContainer="
            "&$OpxTextArea="
            "&$OpxWorkAreaHeader="
            "&$Opycosmoscustomscripts="
            "&$OpzMicroDynamicContainerScripts="
            "&$OpzTextIncludes="
            "&$Opzcosmosuiscripts="
            "&$Opzpega_control_attachcontent="
            "&pyEncodedParameters=true"
            "&pzKeepPageMessages=false"
            "&strPHarnessClass=ESTES-OPS-YardMgmt-Work-Task"
            "&strPHarnessPurpose=TabbedScreenFlow7"
            f"&pzHarnessID={self.pzHarnessID}"
            f"&newSectionID=GID_{str(int(time.time()))}"
            "&UITemplatingStatus=Y"
            "&StreamName=TaskIntakeScreen"
            "&BaseReference=pyWorkPage.MetaData"
            "&bClientValidation=true"
            "&FormError=NONE"
            "&pyCustomError=pyCaseErrorSection"
            "&UsingPage=true"
            "&HeaderButtonSectionName=-1"
            "&PagesToRemove="
            "&inStandardsMode=true"
            "&eventSrcSection=Data-Portal.PortalNavigation"
        )
        response = await self.async_client.post(
            url=self.pega_base_url_to_create_task,
            data=data,
            params=params,
            follow_redirects=True
        )

        save_html_to_file(content=response.content, step=3)

        logger.debug(f'step 2 response code: {response.status_code}')
        assert response.status_code == 200

        logger.debug(f'step # 2 response url: {response.url}')

        logger.debug('Create Task - Ending Step # 2')
        return response.text

    async def step3(self):
        logger.debug('Create Task - Starting Step # 3')
        # url = (
        #     "https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/"
        #     "\u0021DCSPA_YardCoordinator?pzFromFrame=pyWorkPage&pzPrimaryPageName=pyWorkPage&"
        #     "pzTransactionId=0bc32965be8e9d897e68cb4c1d4ddbb4&eventSrcSection=Data-Portal-PortalNavigation"
        # )
        # headers = {
        #     "Accept": "*/*",
        #     "Accept-Language": "en-US,en;q=0.9",
        #     "Cache-Control": "no-cache",
        #     "Connection": "keep-alive",
        #     "Content-Type": "application/x-www-form-urlencoded",
        #     "Cookie": (
        #         "Pega-Perf=itkn=14&start&completed={itkn=4&clientd=190&action=action%3Arefresh%7Ckey%3A&calls=1&httpd=148}; "
        #         "Pega-RULES=%09%7Bpd%7DAAAADaZ7Sz3QXT56V7Zx47C5D%2FdVCePEuIil1ZbyGiY4OXMKlttppqFlm9R%2B0xmRBFhkOA%3D%3DA%7Bapp%7D; "
        #         "JSESSIONID=EC4201C7BCE1106B182839EE7803EC4A; "
        #         "NSC_MC-ZBSE-QSE-TTM=ffffffff09173d9245525d5f4f58455e445a4a4229a0"
        #     ),
        #     "DNT": "1",
        #     "Origin": "https://ymg.estes-express.com",
        #     "Pragma": "no-cache",
        #     "Referer": "https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/\u0021STANDARD",
        #     "Sec-Fetch-Dest": "empty",
        #     "Sec-Fetch-Mode": "cors",
        #     "Sec-Fetch-Site": "same-origin",
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        #     "X-Requested-With": "XMLHttpRequest",
        #     "pzBFP": "{v2}4ad194b176c6278069c88839cccd5ca5",
        #     "pzCTkn": "59b617dce43b1d5dd546925fd1be56f7",
        #     "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        #     "sec-ch-ua-mobile": "?0",
        #     "sec-ch-ua-platform": '"Windows"'
        # }
        params = {
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "pzTransactionId": self.pzTransactionId_1,
            # "eventSrcSection": "Data-Portal-PortalNavigation"
        }
        data = (
            "pyActivity=FinishAssignment"
            "&Purpose=TabbedScreenFlow7"
            "&ReadOnly=-1"
            "&HarnessPurpose=TabbedScreenFlow7"
            "&FolderKey="
            "&InputEnabled=false"
            f"&pzCTkn={self.csrf_token}"
            f"&pzBFP={self.fingerprint_token}"
            "&$PpyWorkPage$ppyFormPost=TRUE"
            "&$PpyWorkPage$ppySpecialtyComponentData="
            "&TaskHelpType="
            "&TaskInstructionsCaption=Instructions"
            "&pClientErrors="
            "&HarnessMode=ACTION"
            "&ActionMode="
            "&NewAction=false"
            "&TaskIndex=1"
            "&TaskHTML="
            "&TaskSectionReference=InitializeTask"
            "&TaskStreamType=Rule-Obj-FlowAction"
            "&TaskStatus=InitializeTask"
            "&TaskInstructions="
            "&TaskHelpPresent=false"
            f"&$PpyWorkPage$pMetaData$pDoorNumber={self.door}"
            f"&$PpyWorkPage$pMetaData$pTrailerNumber={self.trailer_number}"
            "&$PnewAssignPage$ppyCurrentActionLabel=InitializeTask"
            "&HarnessType=Perform"
            # "&$PD_pzFeedParams_pa1632792125632029pz$ppySearchText="
            f"{self.PD_pzFeedParams}$ppySearchText="
            "&appendUniqueIdToFileName=true"
            # "&$PD_pzRenderFeedContext_pa1632792172526988pz$ppyPostPage$ppyFileName="
            f"{self.PD_pzRenderFeedContext}$ppyPostPage$ppyFileName="
            # "&$PD_pzRenderFeedContext_pa1632792172526988pz$ppyPostPage$ppyWebStorageAuthFailed="
            f"{self.PD_pzRenderFeedContext}$ppyPostPage$ppyWebStorageAuthFailed="
            "&$POperatorID$ppxInsName=222886"
            "&$PpxThread$ppxCurrentApplicationName=YardMgmt"
            # "&$PD_pzFeedParams_pa1632792125632029pz$ppzShowNotifications="
            f"{self.PD_pzFeedParams}$ppzShowNotifications="
            "&EXPANDEDLGLayoutGrouppyCaseMainInnerS12=1"
            "&LGTypeLGLayoutGrouppyCaseMainInnerS12=tab"
            "&="
            f"&$PpyWorkPage$pMetaData$pTaskType={self.yard_task_type}"
            "&$PpyWorkPage$pMetaData$pZoneTrailer="
            f"&$PpyWorkPage$pMetaData$ppyDescription={self.general_note}"
            # "&$PD_pzRenderFeedContext_pa1632792172526988pz$ppyPostPage$ppyMessage="
            f"&{self.PD_pzRenderFeedContext}$ppyPostPage$ppyMessage="
            "&isDCSPA=true"
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
            "&$OLGBundle="
            "&$OLayoutGroup="
            "&$OMicroDynamicContainer="
            "&$ONewActionSection="
            "&$OPegaSocial="
            "&$OpxMicroDynamicContainer="
            "&$OpxTextArea="
            "&$OpxWorkAreaHeader="
            "&$Opycosmoscustomscripts="
            "&$OpzMicroDynamicContainerScripts="
            "&$OpzTextIncludes="
            "&$Opzcosmosuiscripts="
            "&$Opzpega_control_attachcontent="
            "&eventSrcSection=Data-Portal-PortalNavigation"
            f"&pzHarnessID={self.pzHarnessID}"
            "&isURLReady=true"
            "&UITemplatingStatus=Y"
            "&inStandardsMode=true"
        )
        response = await self.async_client.post(
            url=self.pega_base_url_to_create_task,
            data=data,
            params=params,
            follow_redirects=True
        )

        self.pzTransactionId_2 = get_pzTransactionId(html_content=response.content)

        save_html_to_file(content=response.content, step=4)

        logger.debug(f'step 3 response code: {response.status_code}')

        assert response.status_code == 200 or 303

        logger.debug(f'step # 3 response url: {response.url}')

        logger.debug('Create Task - Ending Step # 3')
        return response.text

    async def step4(self):
        logger.debug('Create Task - Starting Step # 4')
        # headers = {
        #     "Accept": "*/*",
        #     "Accept-Language": "en-US,en;q=0.9",
        #     "Cache-Control": "no-cache",
        #     "Connection": "keep-alive",
        #     "Content-Type": "application/x-www-form-urlencoded",
        #     "Cookie": (
        #         "Pega-Perf=itkn=19&start; Pega-RULES=%09%7Bpd%7DAAAADaZ7Sz3QXT56V7Zx47C5D%2FdVCePEuIil1ZbyGiY4OXMKlttppqFlm9R%2B0xmRBFhkOA%3D%3DA%7Bapp%7D; "
        #         "JSESSIONID=EC4201C7BCE1106B182839EE7803EC4A; "
        #         "NSC_MC-ZBSE-QSE-TTM=ffffffff09173d9245525d5f4f58455e445a4a4229a0"
        #     ),
        #     "DNT": "1",
        #     "Origin": "https://ymg.estes-express.com",
        #     "Pragma": "no-cache",
        #     "Referer": "https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/\u0021STANDARD",
        #     "Sec-Fetch-Dest": "empty",
        #     "Sec-Fetch-Mode": "cors",
        #     "Sec-Fetch-Site": "same-origin",
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        #     "X-Requested-With": "XMLHttpRequest",
        #     "pzBFP": "{v2}4ad194b176c6278069c88839cccd5ca5",
        #     "pzCTkn": "59b617dce43b1d5dd546925fd1be56f7",
        #     "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        #     "sec-ch-ua-mobile": "?0",
        #     "sec-ch-ua-platform": '"Windows"'
        # }
        params = {
            "pzTransactionId": self.pzTransactionId_2,
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "AJAXTrackID": str(self.async_counter),
            # "eventSrcSection": "Data-Portal.PortalNavigation"
        }
        data = (
            "$PpyWorkPage$pPriority=false"
            f"&$PpyWorkPage$ppyApproverName={self.assigned_to}"
            f"&$PpyWorkPage$ppyAssignedToOperator={self.assigned_to_checker_id}"
            f"&$PpyWorkPage$ppyWorkListText1={self.assigned_to}"
            f"&pzuiactionzzz={self.pzuiactionzzz}"
            "&PreActivitiesList=&sectionParam=&ActivityParams=%3D"
            "&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=HOME"
            "&$OCompositeGadget="
            "&$OControlMenu="
            "&$ODesktopWrapperInclude="
            "&$ODeterminePortalTop="
            "&$ODynamicContainerFrameLess="
            "&$ODynamicLayout="
            "&$ODynamicLayoutCell="
            "&$OEvalDOMScripts_Include="
            "&$OGapIdentifier="
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
            "&$OForm="
            "&$OHarness="
            "&$OLGBundle="
            "&$OLayoutGroup="
            "&$OListView_FilterPanel_Btns="
            "&$OListView_header="
            "&$OMicroDynamicContainer="
            "&$OPegaSocial="
            "&$ORepeatingGrid="
            "&$OpxGrid="
            "&$OpxGridBody="
            "&$OpxGridDataCell="
            "&$OpxGridDataRow="
            "&$OpxGridHeaderCell="
            "&$OpxGridHeaderRow="
            "&$OpxHarnessContent="
            "&$OpxHeaderCell="
            "&$OpxMicroDynamicContainer="
            "&$OpxTextArea="
            "&$OpxWorkArea="
            "&$OpxWorkAreaContent="
            "&$OpxWorkAreaHeader="
            "&$OpyDirtyCheckConfirm="
            "&$OpzLocalActionScript="
            "&$OpzMicroDynamicContainerScripts="
            "&$OpzTextIncludes="
            "&$Opzpega_control_attachcontent="
            "&$OpxCheckbox="
            "&$OpxAutoComplete="
            "&$OpxRadioButtons="
            "&$OpzAutoCompleteAGIncludes="
            "&$OGridInc="
            "&$OpzRadiogroupIncludes="
            "&$OListViewIncludes="
            "&$ONewActionSection="
            "&$Opycosmoscustomscripts="
            "&$Opzcosmosuiscripts="
            "&$OCheckbox="
            "&pyEncodedParameters=true"
            "&pzKeepPageMessages=false"
            "&strPHarnessClass=ESTES-OPS-YardMgmt-Work-Task"
            "&strPHarnessPurpose=TabbedScreenFlow7"
            f"&pzHarnessID={self.pzHarnessID}"
            f"&newSectionID=GID_{str(int(time.time()))}"
            "&UITemplatingStatus=Y"
            "&StreamName=SelectUser"
            "&BaseReference="
            "&bClientValidation=true"
            "&FormError=NONE"
            "&pyCustomError=pyCaseErrorSection"
            "&HeaderButtonSectionName=-1"
            "&PagesToRemove="
            "&inStandardsMode=true"
        )
        response = await self.async_client.post(
            url=self.pega_base_url_to_create_task,
            params=params,
            data=data,
            follow_redirects=True
        )

        save_html_to_file(content=response.content, step=5)

        logger.debug(f'step 5 response code: {response.status_code}')

        assert response.status_code == 200 or 303

        logger.debug(f'step # 4 pega url: {self.pega_base_url_to_create_task}')
        logger.debug(f'step # 4 response url: {response.url}')

        logger.debug('Create Task - Ending Step # 4')
        return response.text

    async def step5(self):
        logger.debug('Create Task - Starting Step # 6')
        # url = (
        #     "https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/"
        #     "!DCSPA_YardCoordinator"
        # )
        params = {
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "pzTransactionId": self.pzTransactionId_2,
            "eventSrcSection": "Data-Portal.PortalNavigation",
        }

        # headers = {
        #     "Accept": "*/*",
        #     "Accept-Language": "en-US,en;q=0.9",
        #     "Cache-Control": "no-cache",
        #     "Connection": "keep-alive",
        #     "Content-Type": "application/x-www-form-urlencoded",
        #     # "Cookie": "...",  # Typically handled automatically by 'client.cookies'
        #     "DNT": "1",
        #     "Origin": "https://ymg.estes-express.com",
        #     "Pragma": "no-cache",
        #     "Referer": (
        #         "https://ymg.estes-express.com/"
        #         "prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!STANDARD"
        #     ),
        #     "Sec-Fetch-Dest": "empty",
        #     "Sec-Fetch-Mode": "cors",
        #     "Sec-Fetch-Site": "same-origin",
        #     "User-Agent": (
        #         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        #         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        #     ),
        #     "X-Requested-With": "XMLHttpRequest",
        #     "pzBFP": self.fingerprint_token,
        #     "pzCTkn": self.csrf_token,
        #     "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        #     "sec-ch-ua-mobile": "?0",
        #     "sec-ch-ua-platform": '"Windows"',
        # }

        # Data shown as a raw string in your cURL, but we can do dict or string
        if self.assigned_to != 'workbasket' or self.assigned_to == '' or self.assigned_to is None:
            data = {
            "pyActivity": "FinishAssignment",
            "Purpose": "TabbedScreenFlow7",
            "ReadOnly": "-1",
            "HarnessPurpose": "TabbedScreenFlow7",
            "FolderKey": "",
            "InputEnabled": "false",
            "pzCTkn": self.csrf_token,
            "pzBFP": self.fingerprint_token,
            "$PpyWorkPage$ppyFormPost": "TRUE",
            "$PpyWorkPage$ppySpecialtyComponentData": "",
            "TaskHelpType": "",
            "TaskInstructionsCaption": "Instructions",
            "pClientErrors": "",
            "HarnessMode": "ACTION",
            "ActionMode": "",
            "NewAction": "false",
            "TaskIndex": "1",
            "TaskHTML": "",
            "TaskSectionReference": "SelectUser",
            "TaskStreamType": "Rule-Obj-FlowAction",
            "TaskStatus": "SelectUser",
            "TaskInstructions": "",
            "TaskHelpPresent": "false",
            "$PpyWorkPage$pPriority": "true" if self.priority == 'Hot' else "false",
            "$PpyWorkPage$ppyApproverName": self.assigned_to,
            "$PpyWorkPage$ppyAssignedToOperator": self.assigned_to_checker_id,
            "$PpyWorkPage$ppyWorkListText1": self.assigned_to,
            "$PnewAssignPage$ppyCurrentActionLabel": "Select Priority and User",
            "HarnessType": "Perform",
            # e.g. "PD_pzFeedParams_pa1801534251050571pz"
            # This is a dynamic param that might differ per session:
            f"${self.PD_pzFeedParams}$ppySearchText": "",  # PD_pzFeedParams_pa1801534251050571pz
            "appendUniqueIdToFileName": "true",
            f"${self.PD_pzRenderFeedContext}$ppyPostPage$ppyFileName": "",  # PD_pzRenderFeedContext_pa1801534321172563pz
            f"${self.PD_pzRenderFeedContext}$ppyPostPage$ppyWebStorageAuthFailed": "",  # PD_pzRenderFeedContext_pa1801534321172563pz
            "$POperatorID$ppxInsName": "222886",
            "$PpxThread$ppxCurrentApplicationName": "YardMgmt",
            f"${self.PD_pzFeedParams}$ppzShowNotifications": "",  # PD_pzFeedParams_pa1801534251050571pz
            "EXPANDEDLGLayoutGrouppyCaseMainInnerS12": "1",
            "LGTypeLGLayoutGrouppyCaseMainInnerS12": "tab",
            "": "",
            f"${self.PD_pzRenderFeedContext}$ppyPostPage$ppyMessage": "",  # PD_pzRenderFeedContext_pa1801534321172563pz
            "isDCSPA": "true",
            "$OCompositeGadget": "",
            "$OControlMenu": "",
            "$ODesktopWrapperInclude": "",
            "$ODeterminePortalTop": "",
            "$ODynamicContainerFrameLess": "",
            "$ODynamicLayout": "",
            "$ODynamicLayoutCell": "",
            "$OEvalDOMScripts_Include": "",
            "$OForm": "",
            "$OGapIdentifier": "",
            "$OGridInc": "",
            "$OHarness": "",
            "$OHarnessStaticJSEnd": "",
            "$OHarnessStaticJSStart": "",
            "$OHarnessStaticScriptsClientValidation": "",
            "$OHarnessStaticScriptsExprCal": "",
            "$OLaunchFlow": "",
            "$OMenuBar": "",
            "$OMenuBarOld": "",
            "$OMobileAppNotify": "",
            "$OOperatorPresenceStatusScripts": "",
            "$OPMCPortalStaticScripts": "",
            "$ORepeatingDynamicLayout": "",
            "$OSessionUser": "",
            "$OSurveyStaticScripts": "",
            "$OWorkformStyles": "",
            "$Ocosmoslocale": "",
            "$OmenubarInclude": "",
            "$OpxButton": "",
            "$OpxDisplayText": "",
            "$OpxDropdown": "",
            "$OpxDynamicContainer": "",
            "$OpxHarnessContent": "",
            "$OpxHeaderCell": "",
            "$OpxHidden": "",
            "$OpxIcon": "",
            "$OpxLayoutContainer": "",
            "$OpxLayoutHeader": "",
            "$OpxLink": "",
            "$OpxMenu": "",
            "$OpxNonTemplate": "",
            "$OpxSection": "",
            "$OpxTextInput": "",
            "$OpxVisible": "",
            "$OpxWorkArea": "",
            "$OpxWorkAreaContent": "",
            "$OpyDirtyCheckConfirm": "",
            "$OpyWorkFormStandardEnd": "",
            "$OpyWorkFormStandardStart": "",
            "$Opycosmoscustomstyles": "",
            "$OpzAppLauncher": "",
            "$OpzDecimalInclude": "",
            "$OpzFrameLessDCScripts": "",
            "$OpzHarnessInlineScriptsEnd": "",
            "$OpzHarnessInlineScriptsStart": "",
            "$OpzPegaCompositeGadgetScripts": "",
            "$OpzRuntimeToolsBar": "",
            "$Opzpega_ui_harnesscontext": "",
            "$Ordlincludes": "",
            "$OxmlDocumentInclude": "",
            "$OLGBundle": "",
            "$OLayoutGroup": "",
            "$OMicroDynamicContainer": "",
            "$ONewActionSection": "",
            "$OPegaSocial": "",
            "$OpxMicroDynamicContainer": "",
            "$OpxTextArea": "",
            "$OpxWorkAreaHeader": "",
            "$Opycosmoscustomstyles": "",
            "$OpzMicroDynamicContainerScripts": "",
            "$OpzTextIncludes": "",
            "$Opzcosmosuiscripts": "",
            "$Opzpega_control_attachcontent": "",
            "$OpxAutoComplete": "",
            "$OpxRadioButtons": "",
            "$OpzAutoCompleteAGIncludes": "",
            "$OpzRadiogroupIncludes": "",
            "pzHarnessID": self.pzHarnessID,
            "eventSrcSection": "Data-Portal.PortalNavigation",
            "isURLReady": "true",
            "UITemplatingStatus": "Y",
            "inStandardsMode": "true",
        }
            logger.debug(f'Assigned to Hostler')
        else:
            logger.debug(f'Assigned to Workbasket')
            data = (
                "pyActivity=FinishAssignment"
                "&Purpose=TabbedScreenFlow7"
                "&ReadOnly=-1"
                "&HarnessPurpose=TabbedScreenFlow7"
                "&FolderKey="
                "&InputEnabled=false"
                f"&pzCTkn={self.csrf_token}"
                f"&pzBFP={self.fingerprint_token}"
                "&$PpyWorkPage$ppyFormPost=TRUE"
                "&$PpyWorkPage$ppySpecialtyComponentData="
                "&TaskHelpType="
                "&TaskInstructionsCaption=Instructions"
                "&pClientErrors="
                "&HarnessMode=ACTION"
                "&ActionMode="
                "&NewAction=false"
                "&TaskIndex=1"
                "&TaskHTML="
                "&TaskSectionReference=SelectUser"
                "&TaskStreamType=Rule-Obj-FlowAction"
                "&TaskStatus=SelectUser"
                "&TaskInstructions="
                "&TaskHelpPresent=false"
                "&$PpyWorkPage$pPriority=true"
                "&$PpyWorkPage$ppyApproverName="
                "&$PpyWorkPage$ppyAssignedToOperator="
                "&$PpyWorkPage$ppyWorkListText1="
                "&$PnewAssignPage$ppyCurrentActionLabel=Select%20Priority%20and%20User"
                "&HarnessType=Perform"
                f"&${self.PD_pzFeedParams}$ppySearchText="  # PD_pzFeedParams_pa1842663151210441pz
                "&appendUniqueIdToFileName=true"
                f"&${self.PD_pzRenderFeedContext}$ppyPostPage$ppyFileName="  # PD_pzRenderFeedContext_pa1842663299132158pz
                f"&${self.PD_pzRenderFeedContext}$ppyPostPage$ppyWebStorageAuthFailed="  # PD_pzRenderFeedContext_pa1842663299132158pz
                f"&$POperatorID$ppxInsName=222886"
                "&$PpxThread$ppxCurrentApplicationName=YardMgmt"
                f"&${self.PD_pzFeedParams}$ppzShowNotifications="  # PD_pzFeedParams_pa1842663151210441pz
                "&EXPANDEDLGLayoutGrouppyCaseMainInnerS12=1"
                "&LGTypeLGLayoutGrouppyCaseMainInnerS12=tab"
                "&="
                f"&${self.PD_pzRenderFeedContext}$ppyPostPage$ppyMessage="  # PD_pzRenderFeedContext_pa1842663299132158pz
                "&isDCSPA=true"
                "&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=HOME"
                "&$OCompositeGadget="
                "&$OControlMenu="
                "&$ODesktopWrapperInclude="
                "&$ODeterminePortalTop="
                "&$ODynamicContainerFrameLess="
                "&$ODynamicLayout="
                "&$ODynamicLayoutCell="
                "&$OEvalDOMScripts_Include="
                "&$OGapIdentifier="
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
                "&$OForm="
                "&$OGridInc="
                "&$OHarness="
                "&$OpxHarnessContent="
                "&$OpxHeaderCell="
                "&$OpxWorkArea="
                "&$OpxWorkAreaContent="
                "&$OpyDirtyCheckConfirm="
                "&$OCheckbox="
                "&$OLGBundle="
                "&$OLayoutGroup="
                "&$OListView_FilterPanel_Btns="
                "&$OListView_header="
                "&$OMicroDynamicContainer="
                "&$OPegaSocial="
                "&$ORepeatingGrid="
                "&$OpxGrid="
                "&$OpxGridBody="
                "&$OpxGridDataCell="
                "&$OpxGridDataRow="
                "&$OpxGridHeaderCell="
                "&$OpxGridHeaderRow="
                "&$OpxMicroDynamicContainer="
                "&$OpxTextArea="
                "&$OpxWorkAreaHeader="
                "&$Opycosmoscustomscripts="
                "&$OpzLocalActionScript="
                "&$OpzMicroDynamicContainerScripts="
                "&$OpzTextIncludes="
                "&$Opzcosmosuiscripts="
                "&$Opzpega_control_attachcontent="
                "&$OpxRadioButtons="
                "&$OListViewIncludes="
                "&$ONewActionSection="
                "&$OpxAutoComplete="
                "&$OpzAutoCompleteAGIncludes="
                "&$OlfsInclude="
                "&$OpxCheckbox="
                f"&pzHarnessID={self.pzHarnessID}"
                "&isURLReady=true"
                "&UITemplatingStatus=Y"
                "&inStandardsMode=true"
            )

        response = await self.async_client.post(
            url=self.pega_base_url_to_create_task,
            params=params,
            # headers=headers,
            data=data,
            follow_redirects=True
        )
        save_html_to_file(content=response.content, step=5)
        logger.debug(f'step 5 response code: {response.status_code}')
        logger.debug(f'step # 5 pega url: {self.pega_base_url_to_create_task}')
        logger.debug(f'step 5 response url: {response.url}')

        logger.debug('Create Task - Ending Step # 5')

        return response.text

    async def step6(self):
        params = {
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "pzTransactionId": self.pzTransactionId_2,
        }
        data = (
            "pyActivity=ReloadSection"
            f"&AC_Grid_FilterParamValue={self.assigned_to}"
            "&AC_SrcParams=%7B%22WorkGroup%22%3A%22Portland%20-%20222%22%7D"
            "&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=HOME"
            "&$OCompositeGadget="
            "&$OControlMenu="
            "&$ODesktopWrapperInclude="
            "&$ODeterminePortalTop="
            "&$ODynamicContainerFrameLess="
            "&$ODynamicLayout="
            "&$ODynamicLayoutCell="
            "&$OEvalDOMScripts_Include="
            "&$OGapIdentifier="
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
            "&$OForm="
            "&$OHarness="
            "&$OLGBundle="
            "&$OLayoutGroup="
            "&$OListView_FilterPanel_Btns="
            "&$OListView_header="
            "&$OMicroDynamicContainer="
            "&$OPegaSocial="
            "&$ORepeatingGrid="
            "&$OpxGrid="
            "&$OpxGridBody="
            "&$OpxGridDataCell="
            "&$OpxGridDataRow="
            "&$OpxGridHeaderCell="
            "&$OpxGridHeaderRow="
            "&$OpxHarnessContent="
            "&$OpxHeaderCell="
            "&$OpxMicroDynamicContainer="
            "&$OpxTextArea="
            "&$OpxWorkArea="
            "&$OpxWorkAreaContent="
            "&$OpxWorkAreaHeader="
            "&$OpyDirtyCheckConfirm="
            "&$OpzLocalActionScript="
            "&$OpzMicroDynamicContainerScripts="
            "&$OpzTextIncludes="
            "&$Opzpega_control_attachcontent="
            "&$OpxCheckbox="
            "&$OpxAutoComplete="
            "&$OpxRadioButtons="
            "&$OpzAutoCompleteAGIncludes="
            "&$OGridInc="
            "&$OpzRadiogroupIncludes="
            "&$OListViewIncludes="
            "&$ONewActionSection="
            "&$Opycosmoscustomscripts="
            "&$Opzcosmosuiscripts="
            "&$OCheckbox="
            "&PreActivitiesList="
            "&UITemplatingStatus=N"
            "&StreamClass=Rule-HTML-Section"
            "&bClientValidation=true"
            "&ReadOnly=0"
            "&StreamName=SelectUser"
            "&RenderSingle=InitialRender_EXPANDEDSubSectionSelectUser5_pyApproverName"
            "&AC_PropPage=pyWorkPage"
            "&BaseReference="
            "&inStandardsMode=true"
            f"&pzHarnessID={self.pzHarnessID}"
            "&PreActivity="
            "&PreDataTransform="
        )
        response = await self.async_client.post(
            url=self.pega_base_url_to_create_task,
            params=params,
            # headers=headers,
            data=data,
            follow_redirects=True
        )
        save_html_to_file(content=response.content, step=6)
        logger.debug(f'step 6 response code: {response.status_code}')
        logger.debug(f'step # 6 pega url: {self.pega_base_url_to_create_task}')
        logger.debug(f'step 56 response url: {response.url}')

        logger.debug('Create Task - Ending Step # 6')

        return response.text
