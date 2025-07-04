import time
import uuid

from backend.pega.yard_coordinator.session_manager.debug import save_html_to_file
from backend.pega.yard_coordinator.session_manager.pega_parser import (
    extract_pzuiactionzzz, extract_pz_transaction_id)
from backend.modules.colored_logger import setup_logger

logger = setup_logger(__name__)


class DeleteTask:
    def __init__(self, task_id, session_manager):
        self.task_id = task_id
        logger.info(f"Initializing DeleteTask for task {self.task_id}")
        self.session = session_manager
        self.ajax_track_id = 1
        self.instance_id = self.task_id.replace("T-", "")
        self.content_id = str(uuid.uuid4())
        self.dynamic_container_id = str(uuid.uuid4())
        self.assignment_handle = f"ASSIGN-INTERNAL ESTES-OPS-YARDMGMT-WORK T-{self.task_id}!PZINTERNALCASEFLOW"

    async def run(self):
        await self.step1_submit_search()
        # await self.step2_open_work_by_handle()
        # await self.step3_fetch_history()
        # await self.step4_reload_section()
        # await self.step5_process_action()
        # await self.step6_submit_encoded_action()
        # await self.step7_do_close()
        await self.step8_reactivate_portal()

    async def step1_submit_search(self):
        logger.info("[Alt-1] Submitting encoded search form")

        params = {
            "pzTransactionId": "",
            "pzFromFrame": "",
            "pzPrimaryPageName": "pyPortalHarness",
            "AJAXTrackID": "1",
            "eventSrcSection": "Data-Portal.UserHeader",
        }

        payload = {
            "pzuiactionzzz": self.session.open_work_by_handle_pzuiactionzzz,
            "pySearchString": self.task_id,
            "pzActivityParams": "pySearchString",
            "$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType": "HARNESS",
            "UITemplatingStatus": "N",
            "inStandardsMode": "true",
            "pzHarnessID": self.session.pzHarnessID,
            "eventSrcSection": "Data-Portal.PortalNavigation",
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
            "$Opycosmoscustomscripts": "",
            "$OpzMicroDynamicContainerScripts": "",
            "$OpzTextIncludes": "",
            "$Opzcosmosuiscripts": "",
            "$Opzpega_control_attachcontent": "",
            "$OpxCheckbox": "",
            "$OpxAutoComplete": "",
            "$OpxRadioButtons": "",
            "$OpzAutoCompleteAGIncludes": "",
            "$OCheckbox": ""
        }

        url = self.session.base_url  # + '?AJAXTrackID=1'
        logger.debug(f'[Alt-1] url={url}')
        logger.debug(f'[Alt-1] pzuiactionzzz: {self.session.open_work_by_handle_pzuiactionzzz}')
        logger.debug(f'[Alt-1] task_id: {self.task_id}')
        logger.debug(f'[Alt-1] pzHarnessID: {self.session.pzHarnessID}')

        res = await self.session.async_client.post(url, params=params, data=payload)
        logger.debug(f'[Alt-1] redirected url: {res.url}')
        res = await self.session.async_client.post(res.url, params=params, data=payload)
        logger.debug(f'[Alt-1] redirected url: {res.url}')
        logger.debug(f'[Alt-1] status_code={res.status_code}, content_length={len(res.text)}')
        save_html_to_file(res.text, 101, enabled=self.session.debug_html)

    async def step2_open_work_by_handle(self):
        logger.info("[Alt-2] Opening work by handle")
        url = self.session.base_url.replace("!STANDARD", "!DCSPA_YardCoordinator")
        params = {
            "eventSrcSection": "Data-Portal.PortalNavigation",
        }
        payload = {
            "pyActivity": "@baseclass.doUIAction",
            "isDCSPA": "true",
            "isSDM": "true",
            "action": "openWorkByHandle",
            "key": self.task_id,
            "SkipConflictCheck": "false",
            "reload": "false",
            "api": "openWorkByHandle",
            "contentID": self.content_id,
            "portalName": "YardCoordinator",
            "portalThreadName": "STANDARDD",
            "tabIndex": "1",
            "pzHarnessID": self.session.pzHarnessID,
            "UITemplatingStatus": "Y",
            "inStandardsMode": "true",
            "eventSrcSection": "Data-Portal.PortalNavigation"
        }

        # Add $O-prefixed form keys as blanks
        for key in [
            "CompositeGadget", "ControlMenu", "DesktopWrapperInclude", "DeterminePortalTop",
            "DynamicContainerFrameLess",
            "DynamicLayout", "DynamicLayoutCell", "EvalDOMScripts_Include", "Form", "GapIdentifier", "GridInc",
            "Harness", "HarnessStaticJSEnd", "HarnessStaticJSStart", "HarnessStaticScriptsClientValidation",
            "HarnessStaticScriptsExprCal", "LaunchFlow", "MenuBar", "MenuBarOld", "MobileAppNotify",
            "OperatorPresenceStatusScripts", "PMCPortalStaticScripts", "RepeatingDynamicLayout", "SessionUser",
            "SurveyStaticScripts", "WorkformStyles", "cosmoslocale", "menubarInclude", "pxButton", "pxDisplayText",
            "pxDropdown", "pxDynamicContainer", "pxHarnessContent", "pxHeaderCell", "pxHidden", "pxIcon",
            "pxLayoutContainer", "pxLayoutHeader", "pxLink", "pxMenu", "pxNonTemplate", "pxSection", "pxTextInput",
            "pxVisible", "pxWorkArea", "pxWorkAreaContent", "pyDirtyCheckConfirm", "pyWorkFormStandardEnd",
            "pyWorkFormStandardStart", "pycosmoscustomstyles", "pzAppLauncher", "pzDecimalInclude",
            "pzFrameLessDCScripts", "pzHarnessInlineScriptsEnd", "pzHarnessInlineScriptsStart",
            "pzPegaCompositeGadgetScripts", "pzRuntimeToolsBar", "pzpega_ui_harnesscontext", "rdlincludes",
            "xmlDocumentInclude", "LGBundle", "LayoutGroup", "MicroDynamicContainer", "NewActionSection",
            "PegaSocial", "pxMicroDynamicContainer", "pxTextArea", "pxWorkAreaHeader", "pycosmoscustomscripts",
            "pzMicroDynamicContainerScripts", "pzTextIncludes", "pzcosmosuiscripts", "pzpega_control_attachcontent",
            "pxCheckbox", "pxAutoComplete", "pxRadioButtons", "pzAutoCompleteAGIncludes", "Checkbox"
        ]:
            payload[f"${'O' if not key.startswith('px') else ''}{key}"] = ""
        res = await self.session.async_client.post(url, params=params, data=payload, follow_redirects=True)
        logger.debug(f'[Alt-2] status_code={res.status_code}, content_length={len(res.text)}')
        save_html_to_file(res.text, 102, enabled=self.session.debug_html)

    async def step3_fetch_history(self):
        logger.info("[Alt-3] Fetching case history")
        params = {
            "pzTransactionId": self.session.pzTransactionId,
            "pzFromFrame": "",
            "pzPrimaryPageName": "pyPortalHarness",
            "AJAXTrackID": "2",
            "eventSrcSection": "Data-Portal.UserHeader",
        }

        json_string = (
            '{'
            f'"pyIsCategorizationEnabled":"true",'
            f'"pyIsRowHeightEnabled":"true",'
            f'"pyIsColumnTogglerEnabled":"false",'
            f'"pyIsRefreshListEnabled":"false",'
            f'"pyIsPersonalizationEnabled":"false",'
            f'"pySectionName":"pyCaseHistoryContent",'
            f'"pySectionClass":"Work-",'
            f'"pzCellMethodName":"generateGridCellModes_2",'
            f'"pyRowVisibleCondition":"",'
            f'"pxFilterConditionId":"gridfiltercondition",'
            f'"pyResultsClass":"History-Work-",'
            f'"pyIsSearchEnabled":"false",'
            f'"pyPassCurrentParamPage":"false",'
            f'"pxDataSrcId":"griddatasource",'
            f'"pyID":"{self.instance_id}",'
            f'"pyPageList":"D_pyWorkHistory_pa{self.instance_id}pz.pxResults",'
            f'"isFilteringEnabled":"true",'
            f'"isSortingEnabled":"true",'
            f'"pzCTMethodName":"gridTemplatePartial_2",'
            f'"pyNoOfColumnsCategorized":0,'
            f'"pyIsTableCategorized":"false",'
            f'"pxObjClass":"Pega-UI-Component-Grid-Filter"'
            '}'
        )

        payload = (
            f"pyActivity=pzRunActionWrapper&"
            f"strJSON={json_string}&"
            f"$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&"
            f"$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&"
            f"$OForm=&$OGapIdentifier=&$OGridInc=&$OHarness=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&"
            f"$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&"
            f"$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&"
            f"$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&"
            f"$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&"
            f"$OpxDynamicContainer=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxHidden=&$OpxIcon=&"
            f"$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&"
            f"$OpxTextInput=&$OpxVisible=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpyDirtyCheckConfirm=&"
            f"$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&"
            f"$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&"
            f"$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&"
            f"$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&"
            f"instanceId={self.instance_id}&pzKeepPageMessages=true&UITemplatingStatus=N&inStandardsMode=true&"
            f"pzHarnessID={self.session.pzHarnessID}&pzActivity=pzBuildFilterIcon&skipReturnResponse=true&pySubAction=runAct"
        )

        url = self.session.base_url.replace("!STANDARD", "!DCSPA_YardCoordinator")

        res = await self.session.async_client.post(url, params=params, data=payload)
        logger.debug(f'[Alt-3] status_code={res.status_code}, content_length={len(res.text)}')
        save_html_to_file(res.text, 103, enabled=self.session.debug_html)

    async def step4_reload_section(self):
        logger.info("[Alt-4] Reloading CaseSummary section")

        url = self.session.base_url.replace("!STANDARD", "!DCSPA_YardCoordinator")
        params = {
            "pzTransactionId": self.session.pzTransactionId,
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "AJAXTrackID": self.ajax_track_id,
        }

        payload = (
            "pyActivity=ReloadSection&"
            "$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&"
            "$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&"
            "$OForm=&$OGapIdentifier=&$OGridInc=&$OHarness=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&"
            "$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&"
            "$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&"
            "$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&"
            "$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&"
            "$OpxDynamicContainer=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxHidden=&$OpxIcon=&"
            "$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&"
            "$OpxTextInput=&$OpxVisible=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpyDirtyCheckConfirm=&"
            "$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&"
            "$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart=&"
            "$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&$Opzpega_ui_harnesscontext=&$Ordlincludes=&"
            "$OxmlDocumentInclude=&$OLGBundle=&$OLayoutGroup=&$OListView_FilterPanel_Btns=&$OListView_header=&"
            "$OMicroDynamicContainer=&$OPegaSocial=&$ORepeatingGrid=&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&"
            "$OpxGridDataRow=&$OpxGridHeaderCell=&$OpxGridHeaderRow=&$OpxMicroDynamicContainer=&$OpxTextArea=&"
            "$OpxWorkAreaHeader=&$Opycosmoscustomscripts=&$OpzLocalActionScript=&$OpzMicroDynamicContainerScripts=&"
            "$OpzTextIncludes=&$Opzcosmosuiscripts=&$Opzpega_control_attachcontent=&"
            "PreActivitiesList=&ReadOnly=-1&"
            "StreamName=CaseSummary&StreamClass=Rule-HTML-Section&"
            "strPHarnessClass=ESTES-OPS-YardMgmt-Work-Task&strPHarnessPurpose=Review&"
            "BaseReference=&bClientValidation=true&FieldError=&FormError=NONE&"
            "pyCustomError=pyCaseErrorSection&pzKeepPageMessages=true&"
            "pyCallStreamMethod=pzLayoutContainer_2&pyLayoutMethodName=pzLayoutContainer_2&"
            "UITemplatingStatus=Y&inStandardsMode=true&"
            f"pzHarnessID={self.session.pzHarnessID}&PreActivity=&PreDataTransform="
        )

        res = await self.session.async_client.post(url, params=params, data=payload)
        logger.debug(f'[Alt-4] status_code={res.status_code}, content_length={len(res.text)}')
        save_html_to_file(res.text, 104, enabled=self.session.debug_html)

    async def step5_process_action(self):
        logger.info("[Alt-5] Processing DeleteTask action")

        url = self.session.base_url.replace("!STANDARD", "!STANDARD")
        params = {
            "pzTransactionId": self.session.pzTransactionId or "",
            "pzFromFrame": "",
            "pzPrimaryPageName": "pyPortalHarness",
            "AJAXTrackID": self.ajax_track_id
        }

        payload = (
            "pyActivity=pzRunActionWrapper&=&pzDataTransformParams=&"
            "$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=WORK&"
            "$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&"
            "$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&"
            "$OForm=&$OGapIdentifier=&$OGridInc=&$OHarness=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&"
            "$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&"
            "$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&"
            "$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&"
            "$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer=&$OpxHarnessContent=&"
            "$OpxHeaderCell=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&"
            "$OpxNonTemplate=&$OpxSection=&$OpxTextInput=&$OpxVisible=&$OpxWorkArea=&$OpxWorkAreaContent=&"
            "$OpyDirtyCheckConfirm=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&"
            "$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&"
            "$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&"
            "$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OLGBundle=&$OLayoutGroup=&"
            "$OListView_FilterPanel_Btns=&$OListView_header=&$OMicroDynamicContainer=&$OPegaSocial=&"
            "$ORepeatingGrid=&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&"
            "$OpxGridHeaderRow=&$OpxMicroDynamicContainer=&$OpxTextArea=&$OpxWorkAreaHeader=&$Opycosmoscustomscripts=&"
            "$OpzLocalActionScript=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes=&$Opzcosmosuiscripts=&"
            "$Opzpega_control_attachcontent=&"
            "pzDataTransform=pyPopulateDiscoverableParams&pySubAction=runDT&"
            f"pzHarnessID={self.session.pzHarnessID}&UITemplatingStatus=N&inStandardsMode=true"
        )

        res = await self.session.async_client.post(url, params=params, data=payload)
        logger.debug(f'[Alt-5] status_code={res.status_code}, content_length={len(res.text)}')
        save_html_to_file(res.text, 105, enabled=self.session.debug_html)

        self.session.pzuiactionzzz = extract_pzuiactionzzz(res.text)
        self.session.pzTransactionId = extract_pz_transaction_id(res.text)

        logger.info(f'pzuiactionzzz: {self.session.pzuiactionzzz}')
        logger.info(f'pzTransactionId: {self.session.pzTransactionId}')

    async def step6_submit_encoded_action(self):
        logger.info("[Alt-6] Submitting encoded action")

        url = self.session.base_url.replace("!STANDARD", "!DCSPA_YardCoordinator")
        params = {
            "pzTransactionId": self.session.pzTransactionId,
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "AJAXTrackID": self.ajax_track_id
        }

        payload = (
            f"pyActivity=ProcessAction&"
            f"$PpyWorkPage$ppyInternalAssignmentHandle={self.assignment_handle}&"
            f"HarnessType=Review&Purpose=Review&"
            f"$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&"
            f"$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&"
            f"$OForm=&$OGapIdentifier=&$OGridInc=&$OHarness=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&"
            f"$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&"
            f"$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&"
            f"$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&"
            f"$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer=&$OpxHarnessContent=&"
            f"$OpxHeaderCell=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&"
            f"$OpxNonTemplate=&$OpxSection=&$OpxTextInput=&$OpxVisible=&$OpxWorkArea=&$OpxWorkAreaContent=&"
            f"$OpyDirtyCheckConfirm=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&"
            f"$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&"
            f"$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&"
            f"$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OLGBundle=&$OLayoutGroup=&"
            f"$OListView_FilterPanel_Btns=&$OListView_header=&$OMicroDynamicContainer=&$OPegaSocial=&"
            f"$ORepeatingGrid=&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&"
            f"$OpxGridHeaderRow=&$OpxMicroDynamicContainer=&$OpxTextArea=&$OpxWorkAreaHeader=&$Opycosmoscustomscripts=&"
            f"$OpzLocalActionScript=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes=&$Opzcosmosuiscripts=&"
            f"$Opzpega_control_attachcontent=&"
            f"UITemplatingStatus=Y&NewTaskStatus=DeleteTask&TaskIndex=&StreamType=Rule-HTML-Section&"
            f"FieldError=&FormError=NONE&pyCustomError=pyCaseErrorSection&bExcludeLegacyJS=true&"
            f"ModalSection=pzModalTemplate&modalStyle=&IgnoreSectionSubmit=true&bInvokedFromControl=true&"
            f"BaseReference=&isModalFlowAction=true&bIsModal=true&bIsOverlay=false&"
            f"StreamClass=Rule-HTML-Section&UITemplatingScriptLoad=true&ActionSection=pzModalTemplate&"
            f"pzHarnessID={self.session.pzHarnessID}&inStandardsMode=true"
        )

        res = await self.session.async_client.post(url, params=params, data=payload)
        logger.debug(f'[Alt-6] status_code={res.status_code}, content_length={len(res.text)}')
        save_html_to_file(res.text, 106, enabled=self.session.debug_html)

    async def step7_do_close(self):
        logger.info("[Alt-7] Closing work tab")

        url = self.session.base_url.replace("!STANDARD", "!DCSPA_YardCoordinator")
        params = {
            "pzTransactionId": self.session.pzTransactionId,
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "AJAXTrackID": self.ajax_track_id
        }

        payload = (
            f"pzuiactionzzz={self.session.pzuiactionzzz}&"
            f"AssignmentID={self.assignment_handle}&pzActivityParams=AssignmentID&"
            f"$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&"
            f"$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&"
            f"$OForm=&$OGapIdentifier=&$OGridInc=&$OHarness=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&"
            f"$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&"
            f"$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&"
            f"$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&"
            f"$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer=&$OpxHarnessContent=&"
            f"$OpxHeaderCell=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&"
            f"$OpxNonTemplate=&$OpxSection=&$OpxTextInput=&$OpxVisible=&$OpxWorkArea=&$OpxWorkAreaContent=&"
            f"$OpyDirtyCheckConfirm=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&"
            f"$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&"
            f"$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&"
            f"$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OLGBundle=&$OLayoutGroup=&"
            f"$OListView_FilterPanel_Btns=&$OListView_header=&$OMicroDynamicContainer=&$OPegaSocial=&"
            f"$ORepeatingGrid=&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&"
            f"$OpxGridHeaderRow=&$OpxMicroDynamicContainer=&$OpxTextArea=&$OpxWorkAreaHeader=&$Opycosmoscustomscripts=&"
            f"$OpzLocalActionScript=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes=&$Opzcosmosuiscripts=&"
            f"$Opzpega_control_attachcontent=&"
            f"UITemplatingStatus=N&inStandardsMode=true&pzHarnessID={self.session.pzHarnessID}"
        )

        res = await self.session.async_client.post(url, params=params, data=payload)
        logger.debug(f'[Alt-7] status_code={res.status_code}, content_length={len(res.text)}')
        save_html_to_file(res.text, 107, enabled=self.session.debug_html)

    async def step8_reactivate_portal(self):
        logger.info("[Alt-8] Reactivating portal")

        url = self.session.base_url.replace("!DCSPA_YardCoordinator", "!STANDARD")

        payload = (
            f"isDCSPA=true&api=activate&pzPostData={int(time.time())}&"
            f"pzHarnessID={self.session.pzHarnessID}&"
            f"UITemplatingStatus=Y&inStandardsMode=true"
        )

        res = await self.session.async_client.post(url, data=payload, follow_redirects=True)
        logger.debug(f'[Alt-8] status_code={res.status_code}, content_length={len(res.text)}')
        save_html_to_file(res.text, 108, enabled=self.session.debug_html)

    async def step9_reactivate_confirm(self):
        logger.info("[Alt-9] Final portal confirmation")

        url = self.session.base_url.replace("!DCSPA_YardCoordinator", "!STANDARD")

        payload = (
            f"isDCSPA=true&AJAXTrackID=2&"
            f"$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=WORK&"
            f"$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&"
            f"$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&"
            f"$OForm=&$OGapIdentifier=&$OGridInc=&$OHarness=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&"
            f"$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&"
            f"$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&"
            f"$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&"
            f"$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer=&$OpxHarnessContent=&"
            f"$OpxHeaderCell=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&"
            f"$OpxNonTemplate=&$OpxSection=&$OpxTextInput=&$OpxVisible=&$OpxWorkArea=&$OpxWorkAreaContent=&"
            f"$OpyDirtyCheckConfirm=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&"
            f"$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&"
            f"$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&"
            f"$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OLGBundle=&$OLayoutGroup=&"
            f"$OListView_FilterPanel_Btns=&$OListView_header=&$OMicroDynamicContainer=&$OPegaSocial=&"
            f"$ORepeatingGrid=&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&"
            f"$OpxGridHeaderRow=&$OpxMicroDynamicContainer=&$OpxTextArea=&$OpxWorkAreaHeader=&$Opycosmoscustomscripts=&"
            f"$OpzLocalActionScript=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes=&$Opzcosmosuiscripts=&"
            f"$Opzpega_control_attachcontent=&"
            f"pzPostData={int(time.time())}&isURLReady=true&api=activate&"
            f"UITemplatingStatus=Y&inStandardsMode=true&pzHarnessID={self.session.pzHarnessID}"
        )

        res = await self.session.async_client.post(url, data=payload)
        logger.debug(f'[Alt-9] status_code={res.status_code}, content_length={len(res.text)}')
        save_html_to_file(res.text, 109, enabled=self.session.debug_html)
