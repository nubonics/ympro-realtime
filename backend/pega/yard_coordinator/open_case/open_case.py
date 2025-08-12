import logging
import re
from uuid import uuid4

from backend.pega.yard_coordinator.open_case.case_info_extractor import get_case_info
from backend.pega.yard_coordinator.open_case.task_fields_extractor import extract_selected_fields
from backend.pega.yard_coordinator.session_manager.debug import save_html_to_file

logger = logging.getLogger(__name__)


class OpenCase:
    def __init__(self, session_manager, case_id):
        self.task_data = None
        self.session_manager = session_manager
        self.case_id = case_id
        self.task_store = session_manager.task_store
        self.case_response = None
        self.content_id = str(uuid4())
        self.async_client = session_manager.async_client
        self.base_url = session_manager.base_url
        self.pzHarnessID = session_manager.pzHarnessID
        self.fingerprint_token = session_manager.fingerprint_token
        self.csrf_token = session_manager.csrf_token
        self.details_url = session_manager.details_url
        self.pzTransactionId = None  # Will be extracted from step1

    def get_headers(self):
        headers = self.session_manager.get_standard_headers()
        headers["Referer"] = f"{self.base_url}"
        return headers

    def get_curl_data(self):
        return (
            "pyActivity=%40baseclass.doUIAction"
            "&isDCSPA=true"
            "&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&$ODynamicContainerFrameLess="
            "&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OForm=&$OGapIdentifier=&$OGridInc="
            "&$OHarness=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&$OHarnessStaticScriptsClientValidation="
            "&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify="
            "&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser="
            "&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText="
            "&$OpxDropdown=&$OpxDynamicContainer=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxHidden=&$OpxIcon="
            "&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput="
            "&$OpxVisible=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpyDirtyCheckConfirm=&$OpyWorkFormStandardEnd="
            "&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts="
            "&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts="
            "&$OpzRuntimeToolsBar=&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OCheckbox=&$OLGBundle="
            "&$OLayoutGroup=&$OMicroDynamicContainer=&$ONewActionSection=&$OPegaSocial=&$OpxMicroDynamicContainer="
            "&$OpxTextArea=&$OpxWorkAreaHeader=&$Opycosmoscustomscripts=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes="
            "&$Opzcosmosuiscripts=&$Opzpega_control_attachcontent=&$OpxAutoComplete=&$OpxRadioButtons=&$OpzAutoCompleteAGIncludes="
            "&$OpzRadiogroupIncludes=&$OListView_FilterPanel_Btns=&$OListView_header=&$ORepeatingGrid=&$OlfsInclude="
            "&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&$OpxGridHeaderRow="
            "&$OpzLocalActionScript=&$OpxCheckbox="
            "&isSDM=true"
            "&action=openWorkByHandle"
            f"&key=ESTES-OPS-YARDMGMT-WORK%20{self.case_id}"
            "&SkipConflictCheck=false"
            "&reload=false"
            "&api=openWorkByHandle"
            f"&contentID={self.content_id if self.content_id else ''}"
            "&portalName=YardCoordinator"
            "&portalThreadName=STANDARD"
            "&tabIndex=1"
            f"&pzHarnessID={self.pzHarnessID}"
            "&UITemplatingStatus=Y"
            "&inStandardsMode=true"
        )

    def parse_pzTransactionId(self, html):
        # Try to find pzTransactionId in URLs or input fields
        # 1. Look for ?pzTransactionId=XYZ in links
        match = re.search(r"pzTransactionId=([a-f0-9]{32})", html)
        if match:
            logger.debug(f"Found pzTransactionId in link: {match.group(1)}")
            return match.group(1)
        # 2. Look for input value="XYZ" name="pzTransactionId"
        match = re.search(r'name="pzTransactionId"\s+value="([a-f0-9]{32})"', html)
        if match:
            logger.debug(f"Found pzTransactionId in input: {match.group(1)}")
            return match.group(1)
        logger.warning("Could not find pzTransactionId in step 1 html!")
        return None

    async def step1(self):
        url = f"{self.base_url.replace('STANDARD', 'DCSPA_YardCoordinator')}"
        headers = self.get_headers()
        data = self.get_curl_data()
        logger.debug(f"OpenCase Step 1: Opening case {self.case_id}")
        self.case_response = await self.async_client.post(
            url,
            headers=headers,
            data=data,
            follow_redirects=True
        )
        save_html_to_file(self.case_response.content, step=1000, enabled=self.session_manager.debug_html)
        logger.debug(f"Step 1 response code: {self.case_response.status_code}")
        logger.debug(f"Step 1 response url: {self.case_response.url}")
        if self.case_response.status_code != 200 and self.case_response.status_code != 303:
            logger.error(f"OpenCase step 1 failed: {self.case_response.status_code} {self.case_response.text}")
            raise Exception("Failed to open case")
        self.pzTransactionId = self.parse_pzTransactionId(self.case_response.text)
        logger.info(f"Step 1: Extracted pzTransactionId: {self.pzTransactionId}")
        task_data = get_case_info(html=self.case_response.text)
        task_data['case_id'] = self.case_id
        self.task_data.update(task_data)
        await self.task_store.upsert_task(task_data=self.task_data)

    def get_step2_data(self):
        return (
            "pyActivity=ReloadSection"
            "&D_TeamMembersByWorkGroupPpxResults1colWidthGBL="
            "&D_TeamMembersByWorkGroupPpxResults1colWidthGBR="
            "&PreActivitiesList="
            "&ActivityParams="
            "&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=WORK"
            "&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&$ODynamicContainerFrameLess="
            "&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OForm=&$OGapIdentifier=&$OGridInc="
            "&$OHarness=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&$OHarnessStaticScriptsClientValidation="
            "&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify="
            "&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser="
            "&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText="
            "&$OpxDropdown=&$OpxDynamicContainer=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxHidden=&$OpxIcon="
            "&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput="
            "&$OpxVisible=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpyDirtyCheckConfirm=&$OpyWorkFormStandardEnd="
            "&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts="
            "&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts="
            "&$OpzRuntimeToolsBar=&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OCheckbox=&$OLGBundle="
            "&$OLayoutGroup=&$OMicroDynamicContainer=&$ONewActionSection=&$OPegaSocial=&$OpxMicroDynamicContainer="
            "&$OpxTextArea=&$OpxWorkAreaHeader=&$Opycosmoscustomscripts=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes="
            "&$Opzcosmosuiscripts=&$Opzpega_control_attachcontent=&$OpxAutoComplete=&$OpxRadioButtons=&$OpzAutoCompleteAGIncludes="
            "&$OpzRadiogroupIncludes=&$OListView_FilterPanel_Btns=&$OListView_header=&$ORepeatingGrid=&$OlfsInclude="
            "&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&$OpxGridHeaderRow="
            "&$OpzLocalActionScript=&$OpxCheckbox="
            "&pyEncodedParameters=true"
            "&pzKeepPageMessages=false"
            "&strPHarnessClass=ESTES-OPS-YardMgmt-UIPages"
            "&strPHarnessPurpose=YardCoordinator"
            "&BaseReference="
            "&StreamList=TeamMembersGrid%7CRule-HTML-Section%7C%7C%7C%7CY%7CSID1752358454675%7C%3A"
            "&bClientValidation=true"
            "&PreActivity="
            "&HeaderButtonSectionName=-1"
            "&PagesToRemove="
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
            "&PreDataTransform="
        )

    def get_step2_params(self):
        return {
            "pzFromFrame": "",
            "pzPrimaryPageName": "pyPortalHarness",
            "AJAXTrackID": "1"
        }

    async def step2(self):
        url = f"{self.base_url.replace('DCSPA_YardCoordinator', 'STANDARD')}"
        headers = self.get_headers()
        params = self.get_step2_params()
        data = self.get_step2_data()
        logger.debug(f"OpenCase Step 2: Reload section for case {self.case_id}")
        response = await self.async_client.post(
            url,
            headers=headers,
            params=params,
            data=data,
            follow_redirects=True
        )
        save_html_to_file(response.content, step=1001, enabled=self.session_manager.debug_html)
        logger.debug(f"Step 2 response code: {response.status_code}")
        logger.debug(f"Step 2 response url: {response.url}")
        if response.status_code != 200 and response.status_code != 303:
            logger.error(f"OpenCase step 2 failed: {response.status_code} {response.text}")
            raise Exception("Failed to reload section")
        return response.text

    def get_step3_params(self):
        # Use parsed pzTransactionId from step1
        return {
            "pzTransactionId": self.pzTransactionId or "",
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "AJAXTrackID": "5"
        }

    def get_step3_data(self):
        # Copied from your cURL
        return (
            "pyActivity=pzRunActionWrapper"
            "&strJSON=%7B%22pyIsCategorizationEnabled%22%3A%22true%22%2C%22pyIsRowHeightEnabled%22%3A%22true%22%2C%22pyIsColumnTogglerEnabled%22%3A%22false%22%2C%22pyIsRefreshListEnabled%22%3A%22false%22%2C%22pyIsPersonalizationEnabled%22%3A%22false%22%2C%22pySectionName%22%3A%22pyCaseHistoryContent%22%2C%22pySectionClass%22%3A%22Work-%22%2C%22pzCellMethodName%22%3A%22generateGridCellModes_2%22%2C%22pyRowVisibleCondition%22%3A%22%22%2C%22pxFilterConditionId%22%3A%2260665cc4b0c652fde04b6998c74afec9f77cbe70_47%22%2C%22pyResultsClass%22%3A%22History-Work-%22%2C%22pyIsSearchEnabled%22%3A%22false%22%2C%22pyPassCurrentParamPage%22%3A%22false%22%2C%22pxDataSrcId%22%3A%2260665cc4b0c652fde04b6998c74afec9f77cbe70_46%22%2C%22pyID%22%3A1752358459047%2C%22pyPageList%22%3A%22D_pyWorkHistory_pa1791232925429837pz.pxResults%22%2C%22isFilteringEnabled%22%3A%22true%22%2C%22isSortingEnabled%22%3A%22true%22%2C%22pzCTMethodName%22%3A%22gridTemplatePartial_2%22%2C%22pyNoOfColumnsCategorized%22%3A0%2C%22pyIsTableCategorized%22%3A%22false%22%2C%22pxObjClass%22%3A%22Pega-UI-Component-Grid-Filter%22%2C%22pyColumns%22%3A%5B%7B%22pyLabel%22%3A%22Time%22%2C%22pyPropertyName%22%3A%22.pxTimeCreated%22%2C%22pyDataType%22%3A%22DateTime%22%2C%22pyFilterType%22%3A%22true%22%2C%22pyColumnSorting%22%3A%22true%22%2C%22pyCellWidth%22%3A%22305px%22%2C%22pyInitialOrder%22%3A1%2C%22pyContentType%22%3A%22FIELD%22%2C%22pyFilterPanelSection%22%3A%22pzFilterPanelDateTime%22%2C%22pyMobileFilterPanelSection%22%3A%22pzMobileFilterPanelDateTime%22%2C%22pyColumnVisibility%22%3A%22AV%22%2C%22pyOrder%22%3A1%2C%22pyShow%22%3Atrue%2C%22pxObjClass%22%3A%22Embed-FilterColumn%22%7D%2C%7B%22pyLabel%22%3A%22Description%22%2C%22pyPropertyName%22%3A%22.pyMessageKey%22%2C%22pyDataType%22%3A%22Text%22%2C%22pyFilterType%22%3A%22true%22%2C%22pyColumnSorting%22%3A%22true%22%2C%22pyCellWidth%22%3A%22802px%22%2C%22pyInitialOrder%22%3A2%2C%22pyContentType%22%3A%22FIELD%22%2C%22pyFilterPanelSection%22%3A%22pzFilterPanelText%22%2C%22pyMobileFilterPanelSection%22%3A%22pzMobileFilterPanelText%22%2C%22pyColumnVisibility%22%3A%22IV%22%2C%22pyOrder%22%3A2%2C%22pyShow%22%3Atrue%2C%22pxObjClass%22%3A%22Embed-FilterColumn%22%7D%2C%7B%22pyLabel%22%3A%22Performed%20by%22%2C%22pyPropertyName%22%3A%22.pyPerformer%22%2C%22pyDataType%22%3A%22Text%22%2C%22pyFilterType%22%3A%22true%22%2C%22pyColumnSorting%22%3A%22true%22%2C%22pyCellWidth%22%3A%22174px%22%2C%22pyInitialOrder%22%3A3%2C%22pyContentType%22%3A%22FIELD%22%2C%22pyFilterPanelSection%22%3A%22pzFilterPanelText%22%2C%22pyMobileFilterPanelSection%22%3A%22pzMobileFilterPanelText%22%2C%22pyColumnVisibility%22%3A%22AV%22%2C%22pyOrder%22%3A3%2C%22pyShow%22%3Atrue%2C%22pxObjClass%22%3A%22Embed-FilterColumn%22%7D%5D%2C%22pyIsModified%22%3A%22false%22%7D"
            "&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=HOME"
            "&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&$ODynamicContainerFrameLess="
            "&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OForm=&$OGapIdentifier=&$OGridInc="
            "&$OHarness=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&$OHarnessStaticScriptsClientValidation="
            "&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify="
            "&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser="
            "&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText="
            "&$OpxDropdown=&$OpxDynamicContainer=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxHidden=&$OpxIcon="
            "&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput="
            "&$OpxVisible=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpyDirtyCheckConfirm=&$OpyWorkFormStandardEnd="
            "&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts="
            "&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts="
            "&$OpzRuntimeToolsBar=&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OCheckbox=&$OLGBundle="
            "&$OLayoutGroup=&$OMicroDynamicContainer=&$ONewActionSection=&$OPegaSocial=&$OpxMicroDynamicContainer="
            "&$OpxTextArea=&$OpxWorkAreaHeader=&$Opycosmoscustomscripts=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes="
            "&$Opzcosmosuiscripts=&$Opzpega_control_attachcontent=&$OpxAutoComplete=&$OpxRadioButtons=&$OpzAutoCompleteAGIncludes="
            "&$OpzRadiogroupIncludes=&$OListView_FilterPanel_Btns=&$OListView_header=&$ORepeatingGrid=&$OlfsInclude="
            "&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&$OpxGridHeaderRow="
            "&$OpzLocalActionScript=&$OpxCheckbox="
            "&instanceId=1752358459047"
            "&pzKeepPageMessages=true"
            "&UITemplatingStatus=N"
            "&inStandardsMode=true"
            "&pzHarnessID=HID1A7315DCDE90282A2EA6F50A868908A9"
            "&pzActivity=pzBuildFilterIcon"
            "&skipReturnResponse=true"
            "&pySubAction=runAct"
        )

    async def step3(self):
        url = f"{self.base_url.replace('STANDARD', 'DCSPA_YardCoordinator')}"
        headers = self.get_headers()
        params = self.get_step3_params()
        data = self.get_step3_data()
        logger.debug(f"OpenCase Step 3: Case history section for case {self.case_id}")
        response = await self.async_client.post(
            url,
            headers=headers,
            params=params,
            data=data,
            follow_redirects=True
        )
        save_html_to_file(response.content, step=1002, enabled=self.session_manager.debug_html)
        logger.debug(f"Step 3 response code: {response.status_code}")
        logger.debug(f"Step 3 response url: {response.url}")
        if response.status_code != 200 and response.status_code != 303:
            logger.error(f"OpenCase step 3 failed: {response.status_code} {response.text}")
            raise Exception("Failed to load case history section")
        return response.text

    def get_step4_params(self):
        # Same as step 3 for params
        return {
            "pzTransactionId": self.pzTransactionId or "",
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "AJAXTrackID": "5"
        }

    def get_step4_data(self):
        # From your step 4 --data-raw
        return (
            "pyActivity=ReloadSection"
            "&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=HOME"
            "&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&$ODynamicContainerFrameLess="
            "&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OForm=&$OGapIdentifier=&$OGridInc="
            "&$OHarness=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&$OHarnessStaticScriptsClientValidation="
            "&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify="
            "&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser="
            "&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText="
            "&$OpxDropdown=&$OpxDynamicContainer=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxHidden=&$OpxIcon="
            "&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput="
            "&$OpxVisible=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpyDirtyCheckConfirm=&$OpyWorkFormStandardEnd="
            "&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts="
            "&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts="
            "&$OpzRuntimeToolsBar=&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OCheckbox=&$OLGBundle="
            "&$OLayoutGroup=&$OMicroDynamicContainer=&$ONewActionSection=&$OPegaSocial=&$OpxMicroDynamicContainer="
            "&$OpxTextArea=&$OpxWorkAreaHeader=&$Opycosmoscustomscripts=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes="
            "&$Opzcosmosuiscripts=&$Opzpega_control_attachcontent=&$OpxAutoComplete=&$OpxRadioButtons=&$OpzAutoCompleteAGIncludes="
            "&$OpzRadiogroupIncludes=&$OListView_FilterPanel_Btns=&$OListView_header=&$ORepeatingGrid=&$OlfsInclude="
            "&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&$OpxGridHeaderRow="
            "&$OpzLocalActionScript=&$OpxCheckbox="
            "&PreActivitiesList="
            "&ReadOnly=-1"
            "&StreamName=CaseSummary"
            "&StreamClass=Rule-HTML-Section"
            "&strPHarnessClass=ESTES-OPS-YardMgmt-Work-Task"
            "&strPHarnessPurpose=Review"
            "&BaseReference="
            "&bClientValidation=true"
            "&FieldError="
            "&FormError=NONE"
            "&pyCustomError=pyCaseErrorSection"
            "&pzKeepPageMessages=true"
            "&pyCallStreamMethod=pzLayoutContainer_2"
            "&pyLayoutMethodName=pzLayoutContainer_2"
            "&UITemplatingStatus=Y"
            "&inStandardsMode=true"
            f"&pzHarnessID={self.pzHarnessID}"
            "&PreActivity="
            "&PreDataTransform="
        )

    async def step4(self):
        url = f"{self.base_url.replace('STANDARD', 'DCSPA_YardCoordinator')}"
        headers = self.get_headers()
        params = self.get_step4_params()
        data = self.get_step4_data()
        logger.debug(f"OpenCase Step 4: Case summary section for case {self.case_id}")
        self.case_response = await self.async_client.post(
            url,
            headers=headers,
            params=params,
            data=data,
            follow_redirects=True
        )
        save_html_to_file(self.case_response.content, step=1003, enabled=self.session_manager.debug_html)
        logger.debug(f"Step 4 response code: {self.case_response.status_code}")
        logger.debug(f"Step 4 response url: {self.case_response.url}")
        if self.case_response.status_code != 200 and self.case_response.status_code != 303:
            logger.error(f"OpenCase step 4 failed: {self.case_response.status_code} {self.case_response.text}")
            raise Exception("Failed to load case summary section")
        task_data = extract_selected_fields(html=self.case_response.text)
        task_data['case_id'] = self.case_id
        self.task_data.update(task_data)
        try:
            await self.task_store.upsert_task(task_data=self.task_data)
        except ValueError:
            logger.error(f"Failed to upsert task data for case {self.case_id}")
            logger.error(f"self.task_data: {self.task_data}")
            logger.error(f"task_data: {task_data}")
            raise
        # return self.case_response.text

    async def step5(self):
        await self.async_client.get(self.base_url)

    async def run(self):
        self.task_data = await self.task_store.get_task(self.case_id)
        await self.step1()
        await self.step2()
        await self.step3()
        # response = await self.step4()
        await self.step4()
        await self.step5()
        # return response
