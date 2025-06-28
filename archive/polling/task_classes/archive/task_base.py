import re
import time
from uuid import uuid4

from lxml import html


class TaskBase:
    def __init__(self, task_id):
        self.base_url = None
        self.task_id = task_id

        # Step 1
        # self.pzuiactionzzz = None # THIS WILL BE INHERITED
        self.ThreadName = f'YardCoordinator_TabThread_{str(int(time.time()))}'  # YardCoordinator_TabThread_1739015193540
        self.insHandle = f"ESTES-OPS-YARDMGMT-WORK {self.task_id}"

        # Step 2
        # self.pzHarnessID = None  # THIS WILL BE INHERITED

        # Step 3
        self.pzTransactionId = None
        self.async_counter = 1
        self.pxFilterConditionId = None
        self.pxDataSrcId = None
        self.pyPageList = None
        self.pyInstanceID = str(int(time.time()))

        # Step 4
        # No new params needed

    async def get_task(self):
        await self.step1()
        await self.step2()
        await self.step3()
        await self.step4()

    @staticmethod
    def extract_pzTransactionId(html_content):
        """
        Extracts the pzTransactionId value from a script tag in the provided HTML.
        The value is expected to appear in a URL inside the JavaScript (for example, in deferredVars).

        Returns:
            The pzTransactionId string if found, or None otherwise.
        """
        tree = html.fromstring(html_content)
        # Look for any <script> element that contains the text "pzTransactionId="
        script_elements = tree.xpath("//script[contains(text(), 'pzTransactionId=')]")

        for script in script_elements:
            script_text = script.text_content()
            # Search for a pattern like: pzTransactionId=333dc5011fd764f89b02364d8935fda4
            match = re.search(r'pzTransactionId=([^&"\s]+)', script_text)
            if match:
                return match.group(1)
        return None

    @staticmethod
    def extract_pxFilterConditionId(html_content):
        """
        Extracts the value of pxFilterConditionId from the script tag that contains
        "pega.ui.jittemplate.mergeSectionStore({".

        Returns:
            The value of pxFilterConditionId as a string, or None if not found.
        """
        tree = html.fromstring(html_content)
        # Find the <script> element that includes the target text
        script_elements = tree.xpath("//script[contains(text(), 'pega.ui.jittemplate.mergeSectionStore({')]")

        for script in script_elements:
            script_text = script.text_content()
            # Use a regular expression to find the "pxFilterConditionId" value.
            # It looks for: "pxFilterConditionId": "VALUE"
            match = re.search(r'"pxFilterConditionId"\s*:\s*"([^"]+)"', script_text)
            if match:
                return match.group(1)
        return None

    @staticmethod
    def extract_datasrcid(html_content):
        """
        Extracts the value of "datasrcid" from a script tag in the provided HTML.
        For example, given a JSON-like block in a script, it will extract:
          "datasrcid": "60665cc4b0c652fde04b6998c74afec9f77cbe70_46"
        and return the value "60665cc4b0c652fde04b6998c74afec9f77cbe70_46".

        Returns:
            The datasrcid string if found, otherwise None.
        """
        tree = html.fromstring(html_content)
        # Find any <script> element that contains the substring "datasrcid"
        script_elements = tree.xpath("//script[contains(text(), 'datasrcid')]")

        for script in script_elements:
            script_text = script.text_content()
            # Look for a pattern like: "datasrcid": "60665cc4b0c652fde04b6998c74afec9f77cbe70_46"
            match = re.search(r'"datasrcid"\s*:\s*"([^"]+)"', script_text)
            if match:
                return match.group(1)
        return None

    @staticmethod
    def extract_pyWorkHistory_pxResults(html_content):
        """
        Searches for a key starting with "D_pyWorkHistory_pa" in a script tag (e.g. in a JSON block)
        and returns that key with ".pxResults" appended.

        For example, if the script contains:
          "D_pyWorkHistory_pa1751904791317926pz": { ... }
        the function will return:
          "D_pyWorkHistory_pa1751904791317926pz.pxResults"

        Returns:
            A string with the key plus ".pxResults", or None if not found.
        """
        tree = html.fromstring(html_content)
        # Find any <script> element that mentions the expected key
        script_elements = tree.xpath("//script[contains(text(), 'D_pyWorkHistory_pa')]")
        for script in script_elements:
            script_text = script.text_content()
            # Look for a pattern like: "D_pyWorkHistory_pa1751904791317926pz":
            match = re.search(r'"(D_pyWorkHistory_pa\d+pz)"\s*:', script_text)
            if match:
                key = match.group(1)
                return f"{key}.pxResults"
        return None

    async def step1(self):
        params = {
            "pzuiactionzzz": self.pzuiactionzzz,
            "ThreadName": self.ThreadName,
            "PortalName": "YardCoordinator",
            "actionName": "openWorkByHandle",
            "insHandle": self.insHandle,
            "mSessionThreadName": "default"
        }
        response = await self.async_client.get(self.base_url, params=params)

        return response.text

    async def step2(self):
        params = {}
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
            "&isSDM=true"
            "&action=openWorkByHandle"
            f"&portalName={self.ThreadName}"
            f"&portalThreadName={self.ThreadName}"
            "&tabIndex=1"
            "&api=openWorkByHandle"
            "&SkipConflictCheck=true"
            f"&key={self.insHandle}"
            f"&contentID={uuid4()}"
            f"&dynamicContainerID={uuid4()}"
            "&isURLReady=true"
            "&isReloaded=true"
            f"&pzHarnessID={self.pzHarnessID}"
            "&UITemplatingStatus=Y"
            "&inStandardsMode=true"
        )

        response = await self.async_client.post(
            self.base_url,
            params=params,
            data=data
        )
        content = response.content
        self.pzTransactionId = self.extract_pzTransactionId(html_content=content)
        self.pxFilterConditionId = self.extract_pxFilterConditionId(html_content=content)
        self.pxDataSrcId = self.extract_datasrcid(html_content=content)
        self.pyPageList = self.extract_pyWorkHistory_pxResults(html_content=content)
        del content
        return response.text

    async def step3(self):
        # Query parameters (plain values)
        params = {
            "pzTransactionId": self.pzTransactionId,  # "333dc5011fd764f89b02364d8935fda4"
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "AJAXTrackID": str(self.async_counter)
        }

        # Data provided as a plain dictionary (values are unencoded)
        data = {
            "pyActivity": "pzBuildFilterIcon",
            "strJSON": (
                '{"pyIsCategorizationEnabled":"true",'
                '"pyIsRowHeightEnabled":"true",'
                '"pyIsColumnTogglerEnabled":"false",'
                '"pyIsRefreshListEnabled":"false",'
                '"pyIsPersonalizationEnabled":"false",'
                '"pySectionName":"pyCaseHistoryContent",'
                '"pySectionClass":"Work-",'
                '"pzCellMethodName":"generateGridCellModes_2",'
                '"pyRowVisibleCondition":"",'
                f'"pxFilterConditionId":"{self.pxFilterConditionId}",'  # 60665cc4b0c652fde04b6998c74afec9f77cbe70_47
                '"pyResultsClass":"History-Work-",'
                '"pyIsSearchEnabled":"false",'
                '"pyPassCurrentParamPage":"false",'
                f'"pxDataSrcId":"{self.pxDataSrcId}",'  # 60665cc4b0c652fde04b6998c74afec9f77cbe70_46
                f'"pyID":"{self.pyInstanceID}",'
                f'"pyPageList":"{self.pyPageList}",'  # D_pyWorkHistory_pa1751904791317926pz.pxResults
                '"isFilteringEnabled":"true",'
                '"isSortingEnabled":"true",'
                '"pzCTMethodName":"gridTemplatePartial_2",'
                '"pyNoOfColumnsCategorized":0,'
                '"pyIsTableCategorized":"false",'
                '"pxObjClass":"Pega-UI-Component-Grid-Filter",'
                '"pyColumns":['
                '{"pyLabel":"Time",'
                '"pyPropertyName":".pxTimeCreated",'
                '"pyDataType":"DateTime",'
                '"pyFilterType":"true",'
                '"pyColumnSorting":"true",'
                '"pyCellWidth":"305px",'
                '"pyInitialOrder":1,'
                '"pyContentType":"FIELD",'
                '"pyFilterPanelSection":"pzFilterPanelDateTime",'
                '"pyMobileFilterPanelSection":"pzMobileFilterPanelDateTime",'
                '"pyColumnVisibility":"AV",'
                '"pyOrder":1,'
                '"pyShow":true,'
                '"pxObjClass":"Embed-FilterColumn"},'
                '{"pyLabel":"Description",'
                '"pyPropertyName":".pyMessageKey",'
                '"pyDataType":"Text",'
                '"pyFilterType":"true",'
                '"pyColumnSorting":"true",'
                '"pyCellWidth":"802px",'
                '"pyInitialOrder":2,'
                '"pyContentType":"FIELD",'
                '"pyFilterPanelSection":"pzFilterPanelText",'
                '"pyMobileFilterPanelSection":"pzMobileFilterPanelText",'
                '"pyColumnVisibility":"IV",'
                '"pyOrder":2,'
                '"pyShow":true,'
                '"pxObjClass":"Embed-FilterColumn"},'
                '{"pyLabel":"Performed by",'
                '"pyPropertyName":".pyPerformer",'
                '"pyDataType":"Text",'
                '"pyFilterType":"true",'
                '"pyColumnSorting":"true",'
                '"pyCellWidth":"174px",'
                '"pyInitialOrder":3,'
                '"pyContentType":"FIELD",'
                '"pyFilterPanelSection":"pzFilterPanelText",'
                '"pyMobileFilterPanelSection":"pzMobileFilterPanelText",'
                '"pyColumnVisibility":"AV",'
                '"pyOrder":3,'
                '"pyShow":true,'
                '"pxObjClass":"Embed-FilterColumn"}'
                '],'
                '"pyIsModified":"false"}'
            ),
            "$OCompositeGadget": "",
            "$OControlMenu": "",
            "$ODesktopWrapperInclude": "",
            "$ODeterminePortalTop": "",
            "$ODynamicContainerFrameLess": "",
            "$ODynamicLayout": "",
            "$ODynamicLayoutCell": "",
            "$OEvalDOMScripts_Include": "",
            "$OGapIdentifier": "",
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
            "instanceId": f"{self.pyInstanceID}",  # 1739015272894
            "pzKeepPageMessages": "true",
            "UITemplatingStatus": "N",
            "inStandardsMode": "true",
            "pzHarnessID": f"{self.pzHarnessID}",  # HID9BDC04B04B6DF8F0A1504161A915EE49
            "pzActivity": "pzBuildFilterIcon",
            "skipReturnResponse": "true",
            "pySubAction": "runAct"
        }
        # Execute the POST request (httpx will automatically encode the query parameters and form data)
        response = await self.async_client.post(
            self.base_url,
            params=params,
            data=data
        )

    async def step4(self):
        params = {
            "pzTransactionId": f"{self.pzTransactionId}",
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "AJAXTrackID": str(self.async_counter)
        }

        data = {
            "pyActivity": "ReloadSection",
            "$OCompositeGadget": "",
            "$OControlMenu": "",
            "$ODesktopWrapperInclude": "",
            "$ODeterminePortalTop": "",
            "$ODynamicContainerFrameLess": "",
            "$ODynamicLayout": "",
            "$ODynamicLayoutCell": "",
            "$OEvalDOMScripts_Include": "",
            "$OGapIdentifier": "",
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
            "$OForm": "",
            "$OHarness": "",
            "$OLGBundle": "",
            "$OLayoutGroup": "",
            "$OListView_FilterPanel_Btns": "",
            "$OListView_header": "",
            "$OMicroDynamicContainer": "",
            "$OPegaSocial": "",
            "$ORepeatingGrid": "",
            "$OpxGrid": "",
            "$OpxGridBody": "",
            "$OpxGridDataCell": "",
            "$OpxGridDataRow": "",
            "$OpxGridHeaderCell": "",
            "$OpxGridHeaderRow": "",
            "$OpxHarnessContent": "",
            "$OpxHeaderCell": "",
            "$OpxMicroDynamicContainer": "",
            "$OpxTextArea": "",
            "$OpxWorkArea": "",
            "$OpxWorkAreaContent": "",
            "$OpxWorkAreaHeader": "",
            "$OpyDirtyCheckConfirm": "",
            "$Opycosmoscustomscripts": "",
            "$OpzLocalActionScript": "",
            "$OpzMicroDynamicContainerScripts": "",
            "$OpzTextIncludes": "",
            "$Opzcosmosuiscripts": "",
            "$Opzpega_control_attachcontent": "",
            "PreActivitiesList": "",
            "ReadOnly": "-1",
            "StreamName": "CaseSummary",
            "StreamClass": "Rule-HTML-Section",
            "strPHarnessClass": "ESTES-OPS-YardMgmt-Work-Task",
            "strPHarnessPurpose": "Review",
            "BaseReference": "",
            "bClientValidation": "true",
            "FieldError": "",
            "FormError": "NONE",
            "pyCustomError": "pyCaseErrorSection",
            "pzKeepPageMessages": "true",
            "pyCallStreamMethod": "pzLayoutContainer_2",
            "pyLayoutMethodName": "pzLayoutContainer_2",
            "UITemplatingStatus": "Y",
            "inStandardsMode": "true",
            "pzHarnessID": f"{self.pzHarnessID}",
            "PreActivity": "",
            "PreDataTransform": ""
        }

        # base_url = (
        #     "https://ymg.estes-express.com/prweb/app/YardMgmt_/"
        #     "hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator_TabThread_1739015193540"
        # )

        response = await self.async_client.post(
            self.base_url,
            params=params,
            data=data
        )
        return response.text
