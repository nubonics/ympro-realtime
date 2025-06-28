from backend.services.polling.task_classes.task_base import TaskBase


class TransferTask(TaskBase):
    def __init__(self, parent=None, task_id=None, assigned_to=None):
        super().__init__(task_id)
        self.parent = parent
        self.task_id = task_id
        self.assigned_to = assigned_to

    async def step1(self):
        params = {
            'pzTransactionId': self.pzTransactionId1,  # 7c1cdd192a34f43e2af54f8b5e96328a
            'pzFromFrame': '',
            'pzPrimaryPageName': 'pyDisplayHarness',
            'AJAXTrackID': '4',
        }

        data = {
        'pyActivity': 'pzRunActionWrapper', '$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType': 'WORK',
         '$OCompositeGadget': '', '$OControlMenu': '', '$ODesktopWrapperInclude': '', '$ODeterminePortalTop': '',
         '$ODynamicContainerFrameLess': '', '$ODynamicLayout': '', '$ODynamicLayoutCell': '',
         '$OEvalDOMScripts_Include': '', '$OGapIdentifier': '', '$OHarnessStaticJSEnd': '',
         '$OHarnessStaticJSStart': '', '$OHarnessStaticScriptsClientValidation': '',
         '$OHarnessStaticScriptsExprCal': '', '$OLaunchFlow': '', '$OMenuBar': '', '$OMenuBarOld': '',
         '$OMobileAppNotify': '', '$OOperatorPresenceStatusScripts': '', '$OPMCPortalStaticScripts': '',
         '$ORepeatingDynamicLayout': '', '$OSessionUser': '', '$OSurveyStaticScripts': '', '$OWorkformStyles': '',
         '$Ocosmoslocale': '', '$OmenubarInclude': '', '$OpxButton': '', '$OpxDisplayText': '', '$OpxDropdown': '',
         '$OpxDynamicContainer': '', '$OpxHidden': '', '$OpxIcon': '', '$OpxLayoutContainer': '',
         '$OpxLayoutHeader': '', '$OpxLink': '', '$OpxMenu': '', '$OpxNonTemplate': '', '$OpxSection': '',
         '$OpxTextInput': '', '$OpxVisible': '', '$OpyWorkFormStandardEnd': '', '$OpyWorkFormStandardStart': '',
         '$Opycosmoscustomstyles': '', '$OpzAppLauncher': '', '$OpzDecimalInclude': '', '$OpzFrameLessDCScripts': '',
         '$OpzHarnessInlineScriptsEnd': '', '$OpzHarnessInlineScriptsStart': '', '$OpzPegaCompositeGadgetScripts': '',
         '$OpzRuntimeToolsBar': '', '$Opzpega_ui_harnesscontext': '', '$Ordlincludes': '', '$OxmlDocumentInclude': '',
         '$OForm': '', '$OGridInc': '', '$OHarness': '', '$OpxHarnessContent': '', '$OpxHeaderCell': '',
         '$OpxWorkArea': '', '$OpxWorkAreaContent': '', '$OpyDirtyCheckConfirm': '', '$OCheckbox': '', '$OLGBundle': '',
         '$OLayoutGroup': '', '$OListView_FilterPanel_Btns': '', '$OListView_header': '', '$OMicroDynamicContainer': '',
         '$OPegaSocial': '', '$ORepeatingGrid': '', '$OpxGrid': '', '$OpxGridBody': '', '$OpxGridDataCell': '',
         '$OpxGridDataRow': '', '$OpxGridHeaderCell': '', '$OpxGridHeaderRow': '', '$OpxMicroDynamicContainer': '',
         '$OpxTextArea': '', '$OpxWorkAreaHeader': '', '$Opycosmoscustomscripts': '', '$OpzLocalActionScript': '',
         '$OpzMicroDynamicContainerScripts': '', '$OpzTextIncludes': '', '$Opzcosmosuiscripts': '',
         '$Opzpega_control_attachcontent': '', '$OpxRadioButtons': '', '$OlfsInclude': '', '$OpxCheckbox': '',
         '$OpxAutoComplete': '', '$OpzAutoCompleteAGIncludes': '', '$OListViewIncludes': '',
         '$OpzRadiogroupIncludes': '', 'ThreadName': '',
         'rowPage': 'D_TeamMembersByWorkGroup_pa545105689959488pz.pxResults(8)',
         'Location': 'pyActivity=pzPrepareAssignment&UITemplatingStatus=Y&NewTaskStatus=DisplayUserWorkList&TaskIndex=&StreamType=Rule-HTML-Section&FieldError=&FormError=&pyCustomError=&bExcludeLegacyJS=true&ModalSection=pzModalTemplate&modalStyle=&IgnoreSectionSubmit=true&bInvokedFromControl=true&BaseReference=&isModalFlowAction=true&bIsModal=true&bIsOverlay=false&StreamClass=Rule-HTML-Section&UITemplatingScriptLoad=true&ActionSection=pzModalTemplate&rowPage=D_TeamMembersByWorkGroup_pa545105689959488pz.pxResults(8)&GridAction=true&BaseThread=DCSPA_YardCoordinator&pzHarnessID=HID88142B62BC212424E4D40CD6829A915D',
         'PagesToCopy': 'D_TeamMembersByWorkGroup_pa545105689959488pz',
         'pzHarnessID': 'HIDCCAB89D19BA29146801CB462326E8A4B', 'UITemplatingStatus': 'N', 'inStandardsMode': 'true',
         'pzActivity': 'pzPerformGridAction', 'skipReturnResponse': 'true', 'pySubAction': 'runAct'}

        # response = requests.post(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        #     data=data,
        # )
        response = await self.request(
            request_type='POST',
            endpoint='DCSPA_YardCoordinator',
            params=params,
            data=data
        )

    async def step2(self):
        params = {
            'pzTransactionId': self.pzTransactionId1,
            'pzFromFrame': '',
            'pzPrimaryPageName': 'pyDisplayHarness',
            'AJAXTrackID': '4',
        }

        data = {
        '$PD_FetchWorkListAssignments_pa636257440547215pz$ppxResults$l1$ppySelected': 'true',
         '$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType': 'WORK', '$OCompositeGadget': '',
         '$OControlMenu': '', '$ODesktopWrapperInclude': '', '$ODeterminePortalTop': '',
         '$ODynamicContainerFrameLess': '', '$ODynamicLayout': '', '$ODynamicLayoutCell': '',
         '$OEvalDOMScripts_Include': '', '$OGapIdentifier': '', '$OHarnessStaticJSEnd': '',
         '$OHarnessStaticJSStart': '', '$OHarnessStaticScriptsClientValidation': '',
         '$OHarnessStaticScriptsExprCal': '', '$OLaunchFlow': '', '$OMenuBar': '', '$OMenuBarOld': '',
         '$OMobileAppNotify': '', '$OOperatorPresenceStatusScripts': '', '$OPMCPortalStaticScripts': '',
         '$ORepeatingDynamicLayout': '', '$OSessionUser': '', '$OSurveyStaticScripts': '', '$OWorkformStyles': '',
         '$Ocosmoslocale': '', '$OmenubarInclude': '', '$OpxButton': '', '$OpxDisplayText': '', '$OpxDropdown': '',
         '$OpxDynamicContainer': '', '$OpxHidden': '', '$OpxIcon': '', '$OpxLayoutContainer': '',
         '$OpxLayoutHeader': '', '$OpxLink': '', '$OpxMenu': '', '$OpxNonTemplate': '', '$OpxSection': '',
         '$OpxTextInput': '', '$OpxVisible': '', '$OpyWorkFormStandardEnd': '', '$OpyWorkFormStandardStart': '',
         '$Opycosmoscustomstyles': '', '$OpzAppLauncher': '', '$OpzDecimalInclude': '', '$OpzFrameLessDCScripts': '',
         '$OpzHarnessInlineScriptsEnd': '', '$OpzHarnessInlineScriptsStart': '', '$OpzPegaCompositeGadgetScripts': '',
         '$OpzRuntimeToolsBar': '', '$Opzpega_ui_harnesscontext': '', '$Ordlincludes': '', '$OxmlDocumentInclude': '',
         '$OForm': '', '$OGridInc': '', '$OHarness': '', '$OpxHarnessContent': '', '$OpxHeaderCell': '',
         '$OpxWorkArea': '', '$OpxWorkAreaContent': '', '$OpyDirtyCheckConfirm': '', '$OCheckbox': '', '$OLGBundle': '',
         '$OLayoutGroup': '', '$OListView_FilterPanel_Btns': '', '$OListView_header': '', '$OMicroDynamicContainer': '',
         '$OPegaSocial': '', '$ORepeatingGrid': '', '$OpxGrid': '', '$OpxGridBody': '', '$OpxGridDataCell': '',
         '$OpxGridDataRow': '', '$OpxGridHeaderCell': '', '$OpxGridHeaderRow': '', '$OpxMicroDynamicContainer': '',
         '$OpxTextArea': '', '$OpxWorkAreaHeader': '', '$Opycosmoscustomscripts': '', '$OpzLocalActionScript': '',
         '$OpzMicroDynamicContainerScripts': '', '$OpzTextIncludes': '', '$Opzcosmosuiscripts': '',
         '$Opzpega_control_attachcontent': '', '$OpxRadioButtons': '', '$OlfsInclude': '', '$OpxCheckbox': '',
         '$OpxAutoComplete': '', '$OpzAutoCompleteAGIncludes': '', '$OListViewIncludes': '',
         '$OpzRadiogroupIncludes': '',
         'pzuiactionzzz': 'CXt0cn17RENTUEFfWWFyZENvb3JkaW5hdG9yfTAyY2U1NTc1ODg3NDY1ZWY4YjVmZWE5NTU3MzQ0MTc2ZTA3M2NiYjVhZWNlZjBhNzRjM2JiZTBhZTBiNzMwZTFjNWUxMTE4MGM3M2NjNTgyNDI1ZWE1ZDNiZjBhYTRkNTkwNzNlNjFkZDFiYmRmYjVmMzU3ZmM3MWVjZjQxNmE4*=',
         'pyPropertyTarget': '$PD_FetchWorkListAssignments_pa636257440547215pz$ppxResults$l1$ppySelected',
         'updateDOM': 'true', 'BaseReference': 'D_TeamMembersByWorkGroup_pa545105689959488pz.pxResults(8)',
         'ContextPage': 'D_FetchWorkListAssignments_pa636257440547215pz.pxResults(1)', 'pzKeepPageMessages': 'true',
         'pega_RLindex': '1', 'PVClientVal': 'true', 'UITemplatingStatus': 'N', 'inStandardsMode': 'true',
         'pzHarnessID': 'HIDCCAB89D19BA29146801CB462326E8A4B'}

        # response = requests.post(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        #     data=data,
        # )
        response = await self.request(
            request_type='POST',
            endpoint='DCSPA_YardCoordinator',
            params=params,
            data=data
        )

    async def step3(self):
        params = {
            'pzTransactionId': self.pzTransactionId1,
            'pzFromFrame': '',
            'pzPrimaryPageName': 'pyDisplayHarness',
            'AJAXTrackID': '4',
        }

        data = {
        'pyActivity': 'ReloadSection', 'D_FetchWorkListAssignmentsPpxResults1colWidthGBL': '',
         'D_FetchWorkListAssignmentsPpxResults1colWidthGBR': '', 'SectionIDList': 'GID_1740317157240:',
         '$PD_FetchWorkListAssignments_pa636257440547215pz$ppxResults$l1$ppySelected': 'true',
         'strIndexInList': '[{"pyPropRef":"D_FetchWorkListAssignments_pa636257440547215pz.pxResults(1)"}]',
         'PreActivitiesList': '', 'sectionParam': '',
         'ActivityParams': 'PageListProperty=D_FetchWorkListAssignments_pa636257440547215pz.pxResults&refreshLayout=false&EditRow=false&gridAction=REFRESHROWS&KeepGridMessages=false',
         '$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType': 'WORK', '$OCompositeGadget': '',
         '$OControlMenu': '', '$ODesktopWrapperInclude': '', '$ODeterminePortalTop': '',
         '$ODynamicContainerFrameLess': '', '$ODynamicLayout': '', '$ODynamicLayoutCell': '',
         '$OEvalDOMScripts_Include': '', '$OGapIdentifier': '', '$OHarnessStaticJSEnd': '',
         '$OHarnessStaticJSStart': '', '$OHarnessStaticScriptsClientValidation': '',
         '$OHarnessStaticScriptsExprCal': '', '$OLaunchFlow': '', '$OMenuBar': '', '$OMenuBarOld': '',
         '$OMobileAppNotify': '', '$OOperatorPresenceStatusScripts': '', '$OPMCPortalStaticScripts': '',
         '$ORepeatingDynamicLayout': '', '$OSessionUser': '', '$OSurveyStaticScripts': '', '$OWorkformStyles': '',
         '$Ocosmoslocale': '', '$OmenubarInclude': '', '$OpxButton': '', '$OpxDisplayText': '', '$OpxDropdown': '',
         '$OpxDynamicContainer': '', '$OpxHidden': '', '$OpxIcon': '', '$OpxLayoutContainer': '',
         '$OpxLayoutHeader': '', '$OpxLink': '', '$OpxMenu': '', '$OpxNonTemplate': '', '$OpxSection': '',
         '$OpxTextInput': '', '$OpxVisible': '', '$OpyWorkFormStandardEnd': '', '$OpyWorkFormStandardStart': '',
         '$Opycosmoscustomstyles': '', '$OpzAppLauncher': '', '$OpzDecimalInclude': '', '$OpzFrameLessDCScripts': '',
         '$OpzHarnessInlineScriptsEnd': '', '$OpzHarnessInlineScriptsStart': '', '$OpzPegaCompositeGadgetScripts': '',
         '$OpzRuntimeToolsBar': '', '$Opzpega_ui_harnesscontext': '', '$Ordlincludes': '', '$OxmlDocumentInclude': '',
         '$OForm': '', '$OGridInc': '', '$OHarness': '', '$OpxHarnessContent': '', '$OpxHeaderCell': '',
         '$OpxWorkArea': '', '$OpxWorkAreaContent': '', '$OpyDirtyCheckConfirm': '', '$OCheckbox': '', '$OLGBundle': '',
         '$OLayoutGroup': '', '$OListView_FilterPanel_Btns': '', '$OListView_header': '', '$OMicroDynamicContainer': '',
         '$OPegaSocial': '', '$ORepeatingGrid': '', '$OpxGrid': '', '$OpxGridBody': '', '$OpxGridDataCell': '',
         '$OpxGridDataRow': '', '$OpxGridHeaderCell': '', '$OpxGridHeaderRow': '', '$OpxMicroDynamicContainer': '',
         '$OpxTextArea': '', '$OpxWorkAreaHeader': '', '$Opycosmoscustomscripts': '', '$OpzLocalActionScript': '',
         '$OpzMicroDynamicContainerScripts': '', '$OpzTextIncludes': '', '$Opzcosmosuiscripts': '',
         '$Opzpega_control_attachcontent': '', '$OpxRadioButtons': '', '$OlfsInclude': '', '$OpxCheckbox': '',
         '$OpxAutoComplete': '', '$OpzAutoCompleteAGIncludes': '', '$OListViewIncludes': '',
         '$OpzRadiogroupIncludes': '', 'pzKeepPageMessages': 'false', 'strPHarnessClass': 'ESTES-OPS-YardMgmt-UIPages',
         'strPHarnessPurpose': 'YardDashboard', 'UITemplatingStatus': 'N', 'StreamName': 'WorkListGridsMain',
         'BaseReference': 'D_TeamMembersByWorkGroup_pa545105689959488pz.pxResults(8)',
         'StreamClass': 'Rule-HTML-Section', 'partialRefresh': 'true',
         'partialTrigger': 'editRowD_FetchWorkListAssignments.pxResults1', 'ReadOnly': '0', 'bClientValidation': 'true',
         'PreActivity': 'pzdoGridAction', 'HeaderButtonSectionName': '-1', 'PagesToRemove': '',
         'pzHarnessID': 'HIDCCAB89D19BA29146801CB462326E8A4B', 'inStandardsMode': 'true', 'PreDataTransform': ''}

        # response = requests.post(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        #     data=data,
        # )
        response = await self.request(
            request_type='POST',
            endpoint='DCSPA_YardCoordinator',
            params=params,
            data=data
        )

    async def step4(self):
        params = {
            'pzTransactionId': self.pzTransactionId1,
            'pzFromFrame': '',
            'pzPrimaryPageName': 'pyDisplayHarness',
            'AJAXTrackID': '4',
        }

        data = {
        'D_FetchWorkListAssignmentsPpxResults1colWidthGBL': '', 'D_FetchWorkListAssignmentsPpxResults1colWidthGBR': '',
         '$PD_TeamMembersByWorkGroup_pa545105689959488pz$ppxResults$l8$ppySelected': 'true',
         '$PD_FetchWorkListAssignments_pa636257440547215pz$ppxResults$l1$ppySelected': 'true',
         'pzuiactionzzz': 'CXt0cn17RENTUEFfWWFyZENvb3JkaW5hdG9yfTAyY2U1NTc1ODg3NDY1ZWY4YjVmZWE5NTU3MzQ0MTc2MTU3Y2RjYmQwMDU3NTdhZjJlNzJhMTUxMjQ3N2YxNGYxMzIzMWVjNmNjZjkyNWY3ZTI4MGUwODFlZjA0ODBlZGM0NzI0NjFmYjIzZWZjYTEzMjliNzNhYjgyMjM1NTA3Y2E0OGU0YWI3ZTgwMWI3ODAzNWU4N2Y1MThjNzM4OWIwN2NkNDQ5OTRkMDMwZjM4ZWQ3M2E2ZDczMjljNjAzMDA0OGJjNDFhNzUzZTUxYjMyMmJjZTM2M2U1NmQ3M2U5YWIyYmUxMzY3MzMwMzEwZWExYmQxNDFjMGVhYmMyNTlkMzk1MGFiYzU5NDE0YzBjOGFlOTMwMzFjMWVmODlhNjkwMjA1OWIzNDk5NGQzMzlmYjA0MTllNzkwMmI0YzE4YjY4NzU3NjE3NDIyOTI4MGZiZDEzNGU4ODgxZDM4ZWM4MzdmNWExOWFhNzVlMjA2MTM0ZWJiMTk4ZGRjODMxOQ%3D%3D*',
         'SectionIDList': 'GID_1740317157240:', 'PreActivitiesList': '', 'sectionParam': '', 'ActivityParams': '',
         '$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType': 'WORK', '$OCompositeGadget': '',
         '$OControlMenu': '', '$ODesktopWrapperInclude': '', '$ODeterminePortalTop': '',
         '$ODynamicContainerFrameLess': '', '$ODynamicLayout': '', '$ODynamicLayoutCell': '',
         '$OEvalDOMScripts_Include': '', '$OGapIdentifier': '', '$OHarnessStaticJSEnd': '',
         '$OHarnessStaticJSStart': '', '$OHarnessStaticScriptsClientValidation': '',
         '$OHarnessStaticScriptsExprCal': '', '$OLaunchFlow': '', '$OMenuBar': '', '$OMenuBarOld': '',
         '$OMobileAppNotify': '', '$OOperatorPresenceStatusScripts': '', '$OPMCPortalStaticScripts': '',
         '$ORepeatingDynamicLayout': '', '$OSessionUser': '', '$OSurveyStaticScripts': '', '$OWorkformStyles': '',
         '$Ocosmoslocale': '', '$OmenubarInclude': '', '$OpxButton': '', '$OpxDisplayText': '', '$OpxDropdown': '',
         '$OpxDynamicContainer': '', '$OpxHidden': '', '$OpxIcon': '', '$OpxLayoutContainer': '',
         '$OpxLayoutHeader': '', '$OpxLink': '', '$OpxMenu': '', '$OpxNonTemplate': '', '$OpxSection': '',
         '$OpxTextInput': '', '$OpxVisible': '', '$OpyWorkFormStandardEnd': '', '$OpyWorkFormStandardStart': '',
         '$Opycosmoscustomstyles': '', '$OpzAppLauncher': '', '$OpzDecimalInclude': '', '$OpzFrameLessDCScripts': '',
         '$OpzHarnessInlineScriptsEnd': '', '$OpzHarnessInlineScriptsStart': '', '$OpzPegaCompositeGadgetScripts': '',
         '$OpzRuntimeToolsBar': '', '$Opzpega_ui_harnesscontext': '', '$Ordlincludes': '', '$OxmlDocumentInclude': '',
         '$OForm': '', '$OGridInc': '', '$OHarness': '', '$OpxHarnessContent': '', '$OpxHeaderCell': '',
         '$OpxWorkArea': '', '$OpxWorkAreaContent': '', '$OpyDirtyCheckConfirm': '', '$OCheckbox': '', '$OLGBundle': '',
         '$OLayoutGroup': '', '$OListView_FilterPanel_Btns': '', '$OListView_header': '', '$OMicroDynamicContainer': '',
         '$OPegaSocial': '', '$ORepeatingGrid': '', '$OpxGrid': '', '$OpxGridBody': '', '$OpxGridDataCell': '',
         '$OpxGridDataRow': '', '$OpxGridHeaderCell': '', '$OpxGridHeaderRow': '', '$OpxMicroDynamicContainer': '',
         '$OpxTextArea': '', '$OpxWorkAreaHeader': '', '$Opycosmoscustomscripts': '', '$OpzLocalActionScript': '',
         '$OpzMicroDynamicContainerScripts': '', '$OpzTextIncludes': '', '$Opzcosmosuiscripts': '',
         '$Opzpega_control_attachcontent': '', '$OpxRadioButtons': '', '$OlfsInclude': '', '$OpxCheckbox': '',
         '$OpxAutoComplete': '', '$OpzAutoCompleteAGIncludes': '', '$OListViewIncludes': '',
         '$OpzRadiogroupIncludes': '', 'pyEncodedParameters': 'true', 'pzKeepPageMessages': 'false',
         'strPHarnessClass': 'ESTES-OPS-YardMgmt-UIPages', 'strPHarnessPurpose': 'YardDashboard',
         'UITemplatingStatus': 'N', 'StreamName': 'WorkListGridsMain',
         'BaseReference': 'D_TeamMembersByWorkGroup_pa545105689959488pz.pxResults(8)', 'bClientValidation': 'true',
         'HeaderButtonSectionName': '-1', 'PagesToRemove': '', 'pzHarnessID': 'HIDCCAB89D19BA29146801CB462326E8A4B',
         'inStandardsMode': 'true'}

        # response = requests.post(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        #     data=data,
        # )
        response = await self.request(
            request_type='POST',
            endpoint='DCSPA_YardCoordinator',
            params=params,
            data=data
        )

    async def step5(self):
        params = {
            'pzTransactionId': 'cf866f2da0f074f10d5f79d02cb3810f',
            'pzFromFrame': '',
            'pzPrimaryPageName': 'pyDisplayHarness',
            'AJAXTrackID': '4',
        }

        data = {
        'pyActivity': 'SubmitModalFlowAction', '$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType': 'WORK',
         '$OCompositeGadget': '', '$OControlMenu': '', '$ODesktopWrapperInclude': '', '$ODeterminePortalTop': '',
         '$ODynamicContainerFrameLess': '', '$ODynamicLayout': '', '$ODynamicLayoutCell': '',
         '$OEvalDOMScripts_Include': '', '$OGapIdentifier': '', '$OHarnessStaticJSEnd': '',
         '$OHarnessStaticJSStart': '', '$OHarnessStaticScriptsClientValidation': '',
         '$OHarnessStaticScriptsExprCal': '', '$OLaunchFlow': '', '$OMenuBar': '', '$OMenuBarOld': '',
         '$OMobileAppNotify': '', '$OOperatorPresenceStatusScripts': '', '$OPMCPortalStaticScripts': '',
         '$ORepeatingDynamicLayout': '', '$OSessionUser': '', '$OSurveyStaticScripts': '', '$OWorkformStyles': '',
         '$Ocosmoslocale': '', '$OmenubarInclude': '', '$OpxButton': '', '$OpxDisplayText': '', '$OpxDropdown': '',
         '$OpxDynamicContainer': '', '$OpxHidden': '', '$OpxIcon': '', '$OpxLayoutContainer': '',
         '$OpxLayoutHeader': '', '$OpxLink': '', '$OpxMenu': '', '$OpxNonTemplate': '', '$OpxSection': '',
         '$OpxTextInput': '', '$OpxVisible': '', '$OpyWorkFormStandardEnd': '', '$OpyWorkFormStandardStart': '',
         '$Opycosmoscustomstyles': '', '$OpzAppLauncher': '', '$OpzDecimalInclude': '', '$OpzFrameLessDCScripts': '',
         '$OpzHarnessInlineScriptsEnd': '', '$OpzHarnessInlineScriptsStart': '', '$OpzPegaCompositeGadgetScripts': '',
         '$OpzRuntimeToolsBar': '', '$Opzpega_ui_harnesscontext': '', '$Ordlincludes': '', '$OxmlDocumentInclude': '',
         '$OForm': '', '$OGridInc': '', '$OHarness': '', '$OpxHarnessContent': '', '$OpxHeaderCell': '',
         '$OpxWorkArea': '', '$OpxWorkAreaContent': '', '$OpyDirtyCheckConfirm': '', '$OCheckbox': '', '$OLGBundle': '',
         '$OLayoutGroup': '', '$OListView_FilterPanel_Btns': '', '$OListView_header': '', '$OMicroDynamicContainer': '',
         '$OPegaSocial': '', '$ORepeatingGrid': '', '$OpxGrid': '', '$OpxGridBody': '', '$OpxGridDataCell': '',
         '$OpxGridDataRow': '', '$OpxGridHeaderCell': '', '$OpxGridHeaderRow': '', '$OpxMicroDynamicContainer': '',
         '$OpxTextArea': '', '$OpxWorkAreaHeader': '', '$Opycosmoscustomscripts': '', '$OpzLocalActionScript': '',
         '$OpzMicroDynamicContainerScripts': '', '$OpzTextIncludes': '', '$Opzcosmosuiscripts': '',
         '$Opzpega_control_attachcontent': '', '$OpxRadioButtons': '', '$OlfsInclude': '', '$OpxCheckbox': '',
         '$OpxAutoComplete': '', '$OpzAutoCompleteAGIncludes': '', '$OListViewIncludes': '',
         '$OpzRadiogroupIncludes': '', 'actionName': '', 'KeepMessages': 'false',
         'ModalActionName': 'DisplayUserWorkList', 'modalSection': 'pzModalTemplate', 'bIsOverlay': 'false',
         'InterestPage': 'D_TeamMembersByWorkGroup_pa545105689959488pz.pxResults(8)', 'HarnessType': 'NEW',
         'UITemplatingStatus': 'Y', 'pzHarnessID': 'HIDCCAB89D19BA29146801CB462326E8A4B', 'inStandardsMode': 'true'}

        # response = requests.post(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        #     data=data,
        # )
        response = await self.request(
            request_type='POST',
            endpoint='DCSPA_YardCoordinator',
            params=params,
            data=data
        )

    async def step6(self):
        params = {
            'pzTransactionId': 'cf866f2da0f074f10d5f79d02cb3810f',
            'pzFromFrame': '',
            'pzPrimaryPageName': 'pyDisplayHarness',
            'AJAXTrackID': '4',
        }

        data = {
        'SubSectionpyGroupBasketWorkBWorkGroup': 'D_PortalContextGlobal.pyActiveWorkGroup',
         'pgRepPgSubSectionpyGroupBasketWorkBPpxResults1colWidthGBL': '',
         'pgRepPgSubSectionpyGroupBasketWorkBPpxResults1colWidthGBR': '', 'EXPANDEDSubSectionpyGroupBasketWorkB': '',
         'SubSectionpyGroupBasketWorkBBWorkGroup': 'D_PortalContextGlobal.pyActiveWorkGroup',
         'pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthGBL': '',
         'pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthGBR': '',
         'pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache1': '',
         'pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache2': '',
         'pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache3': '',
         'pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache4': '',
         'pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache5': '',
         'pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache6': '',
         'pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache7': '',
         'pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache8': '',
         'pgRepPgSubSectionpyGroupBasketWorkBBPpxResults2colWidthCache9': '',
         'pzuiactionzzz': 'CXt0cn17RENTUEFfWWFyZENvb3JkaW5hdG9yfTAyY2U1NTc1ODg3NDY1ZWY4YjVmZWE5NTU3MzQ0MTc2MTU3Y2RjYmQwMDU3NTdhZjJlNzJhMTUxMjQ3N2YxNGYxMzIzMWVjNmNjZjkyNWY3ZTI4MGUwODFlZjA0ODBlZGM0NzI0NjFmYjIzZWZjYTEzMjliNzNhYjgyMjM1NTA3ZWE1OTNhNTllODZjNzAyNzYwNDkxYTJhOWJiZDM4MmZkMzM5ODBiMjljY2Q5ZjgwNWYxN2Y4YjBiMTZjZjc3Yg%3D%3D*',
         'SectionIDList': 'GID_1740317130497:GID_1740317130530:', 'PreActivitiesList': '', 'sectionParam': '',
         'ActivityParams': '=', '$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType': 'WORK',
         '$OCompositeGadget': '', '$OControlMenu': '', '$ODesktopWrapperInclude': '', '$ODeterminePortalTop': '',
         '$ODynamicContainerFrameLess': '', '$ODynamicLayout': '', '$ODynamicLayoutCell': '',
         '$OEvalDOMScripts_Include': '', '$OGapIdentifier': '', '$OHarnessStaticJSEnd': '',
         '$OHarnessStaticJSStart': '', '$OHarnessStaticScriptsClientValidation': '',
         '$OHarnessStaticScriptsExprCal': '', '$OLaunchFlow': '', '$OMenuBar': '', '$OMenuBarOld': '',
         '$OMobileAppNotify': '', '$OOperatorPresenceStatusScripts': '', '$OPMCPortalStaticScripts': '',
         '$ORepeatingDynamicLayout': '', '$OSessionUser': '', '$OSurveyStaticScripts': '', '$OWorkformStyles': '',
         '$Ocosmoslocale': '', '$OmenubarInclude': '', '$OpxButton': '', '$OpxDisplayText': '', '$OpxDropdown': '',
         '$OpxDynamicContainer': '', '$OpxHidden': '', '$OpxIcon': '', '$OpxLayoutContainer': '',
         '$OpxLayoutHeader': '', '$OpxLink': '', '$OpxMenu': '', '$OpxNonTemplate': '', '$OpxSection': '',
         '$OpxTextInput': '', '$OpxVisible': '', '$OpyWorkFormStandardEnd': '', '$OpyWorkFormStandardStart': '',
         '$Opycosmoscustomstyles': '', '$OpzAppLauncher': '', '$OpzDecimalInclude': '', '$OpzFrameLessDCScripts': '',
         '$OpzHarnessInlineScriptsEnd': '', '$OpzHarnessInlineScriptsStart': '', '$OpzPegaCompositeGadgetScripts': '',
         '$OpzRuntimeToolsBar': '', '$Opzpega_ui_harnesscontext': '', '$Ordlincludes': '', '$OxmlDocumentInclude': '',
         '$OForm': '', '$OGridInc': '', '$OHarness': '', '$OpxHarnessContent': '', '$OpxHeaderCell': '',
         '$OpxWorkArea': '', '$OpxWorkAreaContent': '', '$OpyDirtyCheckConfirm': '', '$OCheckbox': '', '$OLGBundle': '',
         '$OLayoutGroup': '', '$OListView_FilterPanel_Btns': '', '$OListView_header': '', '$OMicroDynamicContainer': '',
         '$OPegaSocial': '', '$ORepeatingGrid': '', '$OpxGrid': '', '$OpxGridBody': '', '$OpxGridDataCell': '',
         '$OpxGridDataRow': '', '$OpxGridHeaderCell': '', '$OpxGridHeaderRow': '', '$OpxMicroDynamicContainer': '',
         '$OpxTextArea': '', '$OpxWorkAreaHeader': '', '$Opycosmoscustomscripts': '', '$OpzLocalActionScript': '',
         '$OpzMicroDynamicContainerScripts': '', '$OpzTextIncludes': '', '$Opzcosmosuiscripts': '',
         '$Opzpega_control_attachcontent': '', '$OpxRadioButtons': '', '$OlfsInclude': '', '$OpxCheckbox': '',
         '$OpxAutoComplete': '', '$OpzAutoCompleteAGIncludes': '', '$OListViewIncludes': '',
         '$OpzRadiogroupIncludes': '', 'pyEncodedParameters': 'true', 'pzKeepPageMessages': 'false',
         'strPHarnessClass': 'ESTES-OPS-YardMgmt-UIPages', 'strPHarnessPurpose': 'YardDashboard',
         'UITemplatingStatus': 'Y', 'StreamName': 'pyGroupBasketWork', 'BaseReference': '', 'bClientValidation': 'true',
         'HeaderButtonSectionName': '-1', 'PagesToRemove': '', 'pzHarnessID': 'HIDCCAB89D19BA29146801CB462326E8A4B',
         'inStandardsMode': 'true'}

        # response = requests.post(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        #     data=data,
        # )
        response = await self.request(
            request_type='POST',
            endpoint='DCSPA_YardCoordinator',
            params=params,
            data=data
        )

    async def step7(self):
        params = {
            'pzTransactionId': 'cf866f2da0f074f10d5f79d02cb3810f',
        }

        data = {
        'pyActivity': '@baseclass.doUIAction', 'isDCSPA': 'true', '$OCompositeGadget': '', '$OControlMenu': '',
         '$ODesktopWrapperInclude': '', '$ODeterminePortalTop': '', '$ODynamicContainerFrameLess': '',
         '$ODynamicLayout': '', '$ODynamicLayoutCell': '', '$OEvalDOMScripts_Include': '', '$OGapIdentifier': '',
         '$OHarnessStaticJSEnd': '', '$OHarnessStaticJSStart': '', '$OHarnessStaticScriptsClientValidation': '',
         '$OHarnessStaticScriptsExprCal': '', '$OLaunchFlow': '', '$OMenuBar': '', '$OMenuBarOld': '',
         '$OMobileAppNotify': '', '$OOperatorPresenceStatusScripts': '', '$OPMCPortalStaticScripts': '',
         '$ORepeatingDynamicLayout': '', '$OSessionUser': '', '$OSurveyStaticScripts': '', '$OWorkformStyles': '',
         '$Ocosmoslocale': '', '$OmenubarInclude': '', '$OpxButton': '', '$OpxDisplayText': '', '$OpxDropdown': '',
         '$OpxDynamicContainer': '', '$OpxHidden': '', '$OpxIcon': '', '$OpxLayoutContainer': '',
         '$OpxLayoutHeader': '', '$OpxLink': '', '$OpxMenu': '', '$OpxNonTemplate': '', '$OpxSection': '',
         '$OpxTextInput': '', '$OpxVisible': '', '$OpyWorkFormStandardEnd': '', '$OpyWorkFormStandardStart': '',
         '$Opycosmoscustomstyles': '', '$OpzAppLauncher': '', '$OpzDecimalInclude': '', '$OpzFrameLessDCScripts': '',
         '$OpzHarnessInlineScriptsEnd': '', '$OpzHarnessInlineScriptsStart': '', '$OpzPegaCompositeGadgetScripts': '',
         '$OpzRuntimeToolsBar': '', '$Opzpega_ui_harnesscontext': '', '$Ordlincludes': '', '$OxmlDocumentInclude': '',
         '$OForm': '', '$OGridInc': '', '$OHarness': '', '$OpxHarnessContent': '', '$OpxHeaderCell': '',
         '$OpxWorkArea': '', '$OpxWorkAreaContent': '', '$OpyDirtyCheckConfirm': '', '$OCheckbox': '', '$OLGBundle': '',
         '$OLayoutGroup': '', '$OListView_FilterPanel_Btns': '', '$OListView_header': '', '$OMicroDynamicContainer': '',
         '$OPegaSocial': '', '$ORepeatingGrid': '', '$OpxGrid': '', '$OpxGridBody': '', '$OpxGridDataCell': '',
         '$OpxGridDataRow': '', '$OpxGridHeaderCell': '', '$OpxGridHeaderRow': '', '$OpxMicroDynamicContainer': '',
         '$OpxTextArea': '', '$OpxWorkAreaHeader': '', '$Opycosmoscustomscripts': '', '$OpzLocalActionScript': '',
         '$OpzMicroDynamicContainerScripts': '', '$OpzTextIncludes': '', '$Opzcosmosuiscripts': '',
         '$Opzpega_control_attachcontent': '', '$OpxRadioButtons': '', '$OlfsInclude': '', '$OpxCheckbox': '',
         '$OpxAutoComplete': '', '$OpzAutoCompleteAGIncludes': '', '$OListViewIncludes': '',
         '$OpzRadiogroupIncludes': '', 'isSDM': 'true', 'action': 'openWorkByHandle',
         'key': 'ESTES-OPS-YARDMGMT-WORK T-31320647', 'SkipConflictCheck': 'false', 'reload': 'false',
         'api': 'openWorkByHandle', 'contentID': '23603081-1867-04bc-14e3-322e4e5710ac',
         'portalName': 'YardCoordinator', 'portalThreadName': 'STANDARD', 'tabIndex': '1',
         'pzHarnessID': 'HIDCCAB89D19BA29146801CB462326E8A4B', 'UITemplatingStatus': 'Y', 'inStandardsMode': 'true'}

        # response = requests.post(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        #     data=data,
        # )
        response = await self.request(
            request_type='POST',
            endpoint='DCSPA_YardCoordinator',
            params=params,
            data=data
        )

    async def step8(self):
        params = {
            'pzTransactionId': 'fa451240bc89c7e4fe7671b2cf14c4fe',
            'pzFromFrame': '',
            'pzPrimaryPageName': 'pyPortalHarness',
            'AJAXTrackID': '2',
        }

        data = {
        'pyActivity': 'ReloadSection', 'D_TeamMembersByWorkGroupPpxResults1colWidthGBL': '',
         'D_TeamMembersByWorkGroupPpxResults1colWidthGBR': '', 'PreActivitiesList': '', 'ActivityParams': '',
         '$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType': 'HARNESS', '$OCompositeGadget': '',
         '$OControlMenu': '', '$ODesktopWrapperInclude': '', '$ODeterminePortalTop': '',
         '$ODynamicContainerFrameLess': '', '$ODynamicLayout': '', '$ODynamicLayoutCell': '',
         '$OEvalDOMScripts_Include': '', '$OGapIdentifier': '', '$OHarnessStaticJSEnd': '',
         '$OHarnessStaticJSStart': '', '$OHarnessStaticScriptsClientValidation': '',
         '$OHarnessStaticScriptsExprCal': '', '$OLaunchFlow': '', '$OMenuBar': '', '$OMenuBarOld': '',
         '$OMobileAppNotify': '', '$OOperatorPresenceStatusScripts': '', '$OPMCPortalStaticScripts': '',
         '$ORepeatingDynamicLayout': '', '$OSessionUser': '', '$OSurveyStaticScripts': '', '$OWorkformStyles': '',
         '$Ocosmoslocale': '', '$OmenubarInclude': '', '$OpxButton': '', '$OpxDisplayText': '', '$OpxDropdown': '',
         '$OpxDynamicContainer': '', '$OpxHidden': '', '$OpxIcon': '', '$OpxLayoutContainer': '',
         '$OpxLayoutHeader': '', '$OpxLink': '', '$OpxMenu': '', '$OpxNonTemplate': '', '$OpxSection': '',
         '$OpxTextInput': '', '$OpxVisible': '', '$OpyWorkFormStandardEnd': '', '$OpyWorkFormStandardStart': '',
         '$Opycosmoscustomstyles': '', '$OpzAppLauncher': '', '$OpzDecimalInclude': '', '$OpzFrameLessDCScripts': '',
         '$OpzHarnessInlineScriptsEnd': '', '$OpzHarnessInlineScriptsStart': '', '$OpzPegaCompositeGadgetScripts': '',
         '$OpzRuntimeToolsBar': '', '$Opzpega_ui_harnesscontext': '', '$Ordlincludes': '', '$OxmlDocumentInclude': '',
         '$OForm': '', '$OGridInc': '', '$OHarness': '', '$OpxHarnessContent': '', '$OpxHeaderCell': '',
         '$OpxWorkArea': '', '$OpxWorkAreaContent': '', '$OpyDirtyCheckConfirm': '', '$OCheckbox': '', '$OLGBundle': '',
         '$OLayoutGroup': '', '$OListView_FilterPanel_Btns': '', '$OListView_header': '', '$OMicroDynamicContainer': '',
         '$OPegaSocial': '', '$ORepeatingGrid': '', '$OpxGrid': '', '$OpxGridBody': '', '$OpxGridDataCell': '',
         '$OpxGridDataRow': '', '$OpxGridHeaderCell': '', '$OpxGridHeaderRow': '', '$OpxMicroDynamicContainer': '',
         '$OpxTextArea': '', '$OpxWorkAreaHeader': '', '$Opycosmoscustomscripts': '', '$OpzLocalActionScript': '',
         '$OpzMicroDynamicContainerScripts': '', '$OpzTextIncludes': '', '$Opzcosmosuiscripts': '',
         '$Opzpega_control_attachcontent': '', '$OpxRadioButtons': '', '$OlfsInclude': '', '$OpxCheckbox': '',
         '$OpxAutoComplete': '', '$OpzAutoCompleteAGIncludes': '', '$OListViewIncludes': '',
         '$OpzRadiogroupIncludes': '', 'pyEncodedParameters': 'true', 'pzKeepPageMessages': 'false',
         'strPHarnessClass': 'ESTES-OPS-YardMgmt-UIPages', 'strPHarnessPurpose': 'YardCoordinator', 'BaseReference': '',
         'StreamList': 'TeamMembersGrid|Rule-HTML-Section||||Y|SID1740317128558|:', 'bClientValidation': 'true',
         'PreActivity': '', 'HeaderButtonSectionName': '-1', 'PagesToRemove': '',
         'pzHarnessID': 'HIDAFE941E341451946936AC79C109819DF', 'inStandardsMode': 'true', 'PreDataTransform': ''}

        # response = requests.post(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!STANDARD',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        #     data=data,
        # )
        response = await self.request(
            request_type='POST',
            endpoint='STANDARD',
            params=params,
            data=data
        )

    async def step9(self):
        params = {
            'pzTransactionId': 'cf866f2da0f074f10d5f79d02cb3810f',
            'pzFromFrame': 'pyWorkPage',
            'pzPrimaryPageName': 'pyWorkPage',
            'AJAXTrackID': '5',
        }

        data = {
        'pyActivity': 'pzRunActionWrapper',
         'strJSON': '{"pyIsCategorizationEnabled":"true","pyIsRowHeightEnabled":"true","pyIsColumnTogglerEnabled":"false","pyIsRefreshListEnabled":"false","pyIsPersonalizationEnabled":"false","pySectionName":"pyCaseHistoryContent","pySectionClass":"Work-","pzCellMethodName":"generateGridCellModes_2","pyRowVisibleCondition":"","pxFilterConditionId":"60665cc4b0c652fde04b6998c74afec9f77cbe70_47","pyResultsClass":"History-Work-","pyIsSearchEnabled":"false","pyPassCurrentParamPage":"false","pxDataSrcId":"60665cc4b0c652fde04b6998c74afec9f77cbe70_46","pyID":1740317168736,"pyPageList":"D_pyWorkHistory_pa636268583143257pz.pxResults","isFilteringEnabled":"true","isSortingEnabled":"true","pzCTMethodName":"gridTemplatePartial_2","pyNoOfColumnsCategorized":0,"pyIsTableCategorized":"false","pxObjClass":"Pega-UI-Component-Grid-Filter","pyColumns":[{"pyLabel":"Time","pyPropertyName":".pxTimeCreated","pyDataType":"DateTime","pyFilterType":"true","pyColumnSorting":"true","pyCellWidth":"305px","pyInitialOrder":1,"pyContentType":"FIELD","pyFilterPanelSection":"pzFilterPanelDateTime","pyMobileFilterPanelSection":"pzMobileFilterPanelDateTime","pyColumnVisibility":"AV","pyOrder":1,"pyShow":true,"pxObjClass":"Embed-FilterColumn"},{"pyLabel":"Description","pyPropertyName":".pyMessageKey","pyDataType":"Text","pyFilterType":"true","pyColumnSorting":"true","pyCellWidth":"802px","pyInitialOrder":2,"pyContentType":"FIELD","pyFilterPanelSection":"pzFilterPanelText","pyMobileFilterPanelSection":"pzMobileFilterPanelText","pyColumnVisibility":"IV","pyOrder":2,"pyShow":true,"pxObjClass":"Embed-FilterColumn"},{"pyLabel":"Performed by","pyPropertyName":".pyPerformer","pyDataType":"Text","pyFilterType":"true","pyColumnSorting":"true","pyCellWidth":"174px","pyInitialOrder":3,"pyContentType":"FIELD","pyFilterPanelSection":"pzFilterPanelText","pyMobileFilterPanelSection":"pzMobileFilterPanelText","pyColumnVisibility":"AV","pyOrder":3,"pyShow":true,"pxObjClass":"Embed-FilterColumn"}],"pyIsModified":"false"}',
         '$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType': 'WORK', '$OCompositeGadget': '',
         '$OControlMenu': '', '$ODesktopWrapperInclude': '', '$ODeterminePortalTop': '',
         '$ODynamicContainerFrameLess': '', '$ODynamicLayout': '', '$ODynamicLayoutCell': '',
         '$OEvalDOMScripts_Include': '', '$OGapIdentifier': '', '$OHarnessStaticJSEnd': '',
         '$OHarnessStaticJSStart': '', '$OHarnessStaticScriptsClientValidation': '',
         '$OHarnessStaticScriptsExprCal': '', '$OLaunchFlow': '', '$OMenuBar': '', '$OMenuBarOld': '',
         '$OMobileAppNotify': '', '$OOperatorPresenceStatusScripts': '', '$OPMCPortalStaticScripts': '',
         '$ORepeatingDynamicLayout': '', '$OSessionUser': '', '$OSurveyStaticScripts': '', '$OWorkformStyles': '',
         '$Ocosmoslocale': '', '$OmenubarInclude': '', '$OpxButton': '', '$OpxDisplayText': '', '$OpxDropdown': '',
         '$OpxDynamicContainer': '', '$OpxHidden': '', '$OpxIcon': '', '$OpxLayoutContainer': '',
         '$OpxLayoutHeader': '', '$OpxLink': '', '$OpxMenu': '', '$OpxNonTemplate': '', '$OpxSection': '',
         '$OpxTextInput': '', '$OpxVisible': '', '$OpyWorkFormStandardEnd': '', '$OpyWorkFormStandardStart': '',
         '$Opycosmoscustomstyles': '', '$OpzAppLauncher': '', '$OpzDecimalInclude': '', '$OpzFrameLessDCScripts': '',
         '$OpzHarnessInlineScriptsEnd': '', '$OpzHarnessInlineScriptsStart': '', '$OpzPegaCompositeGadgetScripts': '',
         '$OpzRuntimeToolsBar': '', '$Opzpega_ui_harnesscontext': '', '$Ordlincludes': '', '$OxmlDocumentInclude': '',
         '$OForm': '', '$OGridInc': '', '$OHarness': '', '$OpxHarnessContent': '', '$OpxHeaderCell': '',
         '$OpxWorkArea': '', '$OpxWorkAreaContent': '', '$OpyDirtyCheckConfirm': '', '$OCheckbox': '', '$OLGBundle': '',
         '$OLayoutGroup': '', '$OListView_FilterPanel_Btns': '', '$OListView_header': '', '$OMicroDynamicContainer': '',
         '$OPegaSocial': '', '$ORepeatingGrid': '', '$OpxGrid': '', '$OpxGridBody': '', '$OpxGridDataCell': '',
         '$OpxGridDataRow': '', '$OpxGridHeaderCell': '', '$OpxGridHeaderRow': '', '$OpxMicroDynamicContainer': '',
         '$OpxTextArea': '', '$OpxWorkAreaHeader': '', '$Opycosmoscustomscripts': '', '$OpzLocalActionScript': '',
         '$OpzMicroDynamicContainerScripts': '', '$OpzTextIncludes': '', '$Opzcosmosuiscripts': '',
         '$Opzpega_control_attachcontent': '', '$OpxRadioButtons': '', '$OlfsInclude': '', '$OpxCheckbox': '',
         '$OpxAutoComplete': '', '$OpzAutoCompleteAGIncludes': '', '$OListViewIncludes': '',
         '$OpzRadiogroupIncludes': '', 'instanceId': '1740317168736', 'pzKeepPageMessages': 'true',
         'UITemplatingStatus': 'N', 'inStandardsMode': 'true', 'pzHarnessID': 'HID910FB64868A38C3F75F0EB6A57FD50A3',
         'pzActivity': 'pzBuildFilterIcon', 'skipReturnResponse': 'true', 'pySubAction': 'runAct'}

        # response = requests.post(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        #     data=data,
        # )
        response = await self.request(
            request_type='POST',
            endpoint='DCSPA_YardCoordinator',
            params=params,
            data=data
        )

    async def step10(self):
        params = {
            'pzTransactionId': 'cf866f2da0f074f10d5f79d02cb3810f',
            'pzFromFrame': 'pyWorkPage',
            'pzPrimaryPageName': 'pyWorkPage',
            'AJAXTrackID': '5',
        }

        data = {
        'pyActivity': 'ReloadSection', '$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType': 'WORK',
         '$OCompositeGadget': '', '$OControlMenu': '', '$ODesktopWrapperInclude': '', '$ODeterminePortalTop': '',
         '$ODynamicContainerFrameLess': '', '$ODynamicLayout': '', '$ODynamicLayoutCell': '',
         '$OEvalDOMScripts_Include': '', '$OGapIdentifier': '', '$OHarnessStaticJSEnd': '',
         '$OHarnessStaticJSStart': '', '$OHarnessStaticScriptsClientValidation': '',
         '$OHarnessStaticScriptsExprCal': '', '$OLaunchFlow': '', '$OMenuBar': '', '$OMenuBarOld': '',
         '$OMobileAppNotify': '', '$OOperatorPresenceStatusScripts': '', '$OPMCPortalStaticScripts': '',
         '$ORepeatingDynamicLayout': '', '$OSessionUser': '', '$OSurveyStaticScripts': '', '$OWorkformStyles': '',
         '$Ocosmoslocale': '', '$OmenubarInclude': '', '$OpxButton': '', '$OpxDisplayText': '', '$OpxDropdown': '',
         '$OpxDynamicContainer': '', '$OpxHidden': '', '$OpxIcon': '', '$OpxLayoutContainer': '',
         '$OpxLayoutHeader': '', '$OpxLink': '', '$OpxMenu': '', '$OpxNonTemplate': '', '$OpxSection': '',
         '$OpxTextInput': '', '$OpxVisible': '', '$OpyWorkFormStandardEnd': '', '$OpyWorkFormStandardStart': '',
         '$Opycosmoscustomstyles': '', '$OpzAppLauncher': '', '$OpzDecimalInclude': '', '$OpzFrameLessDCScripts': '',
         '$OpzHarnessInlineScriptsEnd': '', '$OpzHarnessInlineScriptsStart': '', '$OpzPegaCompositeGadgetScripts': '',
         '$OpzRuntimeToolsBar': '', '$Opzpega_ui_harnesscontext': '', '$Ordlincludes': '', '$OxmlDocumentInclude': '',
         '$OForm': '', '$OGridInc': '', '$OHarness': '', '$OpxHarnessContent': '', '$OpxHeaderCell': '',
         '$OpxWorkArea': '', '$OpxWorkAreaContent': '', '$OpyDirtyCheckConfirm': '', '$OCheckbox': '', '$OLGBundle': '',
         '$OLayoutGroup': '', '$OListView_FilterPanel_Btns': '', '$OListView_header': '', '$OMicroDynamicContainer': '',
         '$OPegaSocial': '', '$ORepeatingGrid': '', '$OpxGrid': '', '$OpxGridBody': '', '$OpxGridDataCell': '',
         '$OpxGridDataRow': '', '$OpxGridHeaderCell': '', '$OpxGridHeaderRow': '', '$OpxMicroDynamicContainer': '',
         '$OpxTextArea': '', '$OpxWorkAreaHeader': '', '$Opycosmoscustomscripts': '', '$OpzLocalActionScript': '',
         '$OpzMicroDynamicContainerScripts': '', '$OpzTextIncludes': '', '$Opzcosmosuiscripts': '',
         '$Opzpega_control_attachcontent': '', '$OpxRadioButtons': '', '$OlfsInclude': '', '$OpxCheckbox': '',
         '$OpxAutoComplete': '', '$OpzAutoCompleteAGIncludes': '', '$OListViewIncludes': '',
         '$OpzRadiogroupIncludes': '', 'PreActivitiesList': '', 'ReadOnly': '-1', 'StreamName': 'CaseSummary',
         'StreamClass': 'Rule-HTML-Section', 'strPHarnessClass': 'ESTES-OPS-YardMgmt-Work-Task',
         'strPHarnessPurpose': 'Review', 'BaseReference': '', 'bClientValidation': 'true', 'FieldError': '',
         'FormError': 'NONE', 'pyCustomError': 'pyCaseErrorSection', 'pzKeepPageMessages': 'true',
         'pyCallStreamMethod': 'pzLayoutContainer_2', 'pyLayoutMethodName': 'pzLayoutContainer_2',
         'UITemplatingStatus': 'Y', 'inStandardsMode': 'true', 'pzHarnessID': 'HID910FB64868A38C3F75F0EB6A57FD50A3',
         'PreActivity': '', 'PreDataTransform': ''}

        # response = requests.post(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        #     data=data,
        # )
        response = await self.request(
            request_type='POST',
            endpoint='DCSPA_YardCoordinator',
            params=params,
            data=data
        )

    async def step11(self):
        params = {
            'pzTransactionId': 'cf866f2da0f074f10d5f79d02cb3810f',
            'pzFromFrame': 'pyWorkPage',
            'pzPrimaryPageName': 'pyWorkPage',
            'AJAXTrackID': '5',
        }

        data = {
        'pyActivity': 'ReloadSection', '$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType': 'WORK',
         '$OCompositeGadget': '', '$OControlMenu': '', '$ODesktopWrapperInclude': '', '$ODeterminePortalTop': '',
         '$ODynamicContainerFrameLess': '', '$ODynamicLayout': '', '$ODynamicLayoutCell': '',
         '$OEvalDOMScripts_Include': '', '$OGapIdentifier': '', '$OHarnessStaticJSEnd': '',
         '$OHarnessStaticJSStart': '', '$OHarnessStaticScriptsClientValidation': '',
         '$OHarnessStaticScriptsExprCal': '', '$OLaunchFlow': '', '$OMenuBar': '', '$OMenuBarOld': '',
         '$OMobileAppNotify': '', '$OOperatorPresenceStatusScripts': '', '$OPMCPortalStaticScripts': '',
         '$ORepeatingDynamicLayout': '', '$OSessionUser': '', '$OSurveyStaticScripts': '', '$OWorkformStyles': '',
         '$Ocosmoslocale': '', '$OmenubarInclude': '', '$OpxButton': '', '$OpxDisplayText': '', '$OpxDropdown': '',
         '$OpxDynamicContainer': '', '$OpxHidden': '', '$OpxIcon': '', '$OpxLayoutContainer': '',
         '$OpxLayoutHeader': '', '$OpxLink': '', '$OpxMenu': '', '$OpxNonTemplate': '', '$OpxSection': '',
         '$OpxTextInput': '', '$OpxVisible': '', '$OpyWorkFormStandardEnd': '', '$OpyWorkFormStandardStart': '',
         '$Opycosmoscustomstyles': '', '$OpzAppLauncher': '', '$OpzDecimalInclude': '', '$OpzFrameLessDCScripts': '',
         '$OpzHarnessInlineScriptsEnd': '', '$OpzHarnessInlineScriptsStart': '', '$OpzPegaCompositeGadgetScripts': '',
         '$OpzRuntimeToolsBar': '', '$Opzpega_ui_harnesscontext': '', '$Ordlincludes': '', '$OxmlDocumentInclude': '',
         '$OForm': '', '$OGridInc': '', '$OHarness': '', '$OpxHarnessContent': '', '$OpxHeaderCell': '',
         '$OpxWorkArea': '', '$OpxWorkAreaContent': '', '$OpyDirtyCheckConfirm': '', '$OCheckbox': '', '$OLGBundle': '',
         '$OLayoutGroup': '', '$OListView_FilterPanel_Btns': '', '$OListView_header': '', '$OMicroDynamicContainer': '',
         '$OPegaSocial': '', '$ORepeatingGrid': '', '$OpxGrid': '', '$OpxGridBody': '', '$OpxGridDataCell': '',
         '$OpxGridDataRow': '', '$OpxGridHeaderCell': '', '$OpxGridHeaderRow': '', '$OpxMicroDynamicContainer': '',
         '$OpxTextArea': '', '$OpxWorkAreaHeader': '', '$Opycosmoscustomscripts': '', '$OpzLocalActionScript': '',
         '$OpzMicroDynamicContainerScripts': '', '$OpzTextIncludes': '', '$Opzcosmosuiscripts': '',
         '$Opzpega_control_attachcontent': '', '$OpxRadioButtons': '', '$OlfsInclude': '', '$OpxCheckbox': '',
         '$OpxAutoComplete': '', '$OpzAutoCompleteAGIncludes': '', '$OListViewIncludes': '',
         '$OpzRadiogroupIncludes': '', 'PreActivitiesList': '', 'StreamName': 'CaseSummary',
         'StreamClass': 'Rule-HTML-Section', 'bClientValidation': 'true', 'BaseReference': '',
         'pzKeepPageMessages': 'true', 'strPHarnessClass': 'ESTES-OPS-YardMgmt-Work-Task',
         'strPHarnessPurpose': 'Review', 'Increment': 'true', 'UITemplatingStatus': 'Y', 'ReadOnly': '-1',
         'pyCallStreamMethod': 'simpleLayout_11', 'pyLayoutMethodName': 'simpleLayout_11', 'inStandardsMode': 'true',
         'pzHarnessID': 'HID910FB64868A38C3F75F0EB6A57FD50A3', 'PreActivity': '', 'PreDataTransform': ''}

        # response = requests.post(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        #     data=data,
        # )
        response = await self.request(
            request_type='POST',
            endpoint='DCSPA_YardCoordinator',
            params=params,
            data=data
        )

    async def step12(self):
        params = {
            'pzTransactionId': 'cf866f2da0f074f10d5f79d02cb3810f',
            'pzFromFrame': 'pyWorkPage',
            'pzPrimaryPageName': 'pyWorkPage',
            'AJAXTrackID': '5',
        }

        data = {
        'pyActivity': 'ReloadSection', 'AC_Grid_FilterParamValue': 'lo',
         'AC_SrcParams': '{"WorkGroup":"Portland - 222"}',
         '$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType': 'WORK', '$OCompositeGadget': '',
         '$OControlMenu': '', '$ODesktopWrapperInclude': '', '$ODeterminePortalTop': '',
         '$ODynamicContainerFrameLess': '', '$ODynamicLayout': '', '$ODynamicLayoutCell': '',
         '$OEvalDOMScripts_Include': '', '$OGapIdentifier': '', '$OHarnessStaticJSEnd': '',
         '$OHarnessStaticJSStart': '', '$OHarnessStaticScriptsClientValidation': '',
         '$OHarnessStaticScriptsExprCal': '', '$OLaunchFlow': '', '$OMenuBar': '', '$OMenuBarOld': '',
         '$OMobileAppNotify': '', '$OOperatorPresenceStatusScripts': '', '$OPMCPortalStaticScripts': '',
         '$ORepeatingDynamicLayout': '', '$OSessionUser': '', '$OSurveyStaticScripts': '', '$OWorkformStyles': '',
         '$Ocosmoslocale': '', '$OmenubarInclude': '', '$OpxButton': '', '$OpxDisplayText': '', '$OpxDropdown': '',
         '$OpxDynamicContainer': '', '$OpxHidden': '', '$OpxIcon': '', '$OpxLayoutContainer': '',
         '$OpxLayoutHeader': '', '$OpxLink': '', '$OpxMenu': '', '$OpxNonTemplate': '', '$OpxSection': '',
         '$OpxTextInput': '', '$OpxVisible': '', '$OpyWorkFormStandardEnd': '', '$OpyWorkFormStandardStart': '',
         '$Opycosmoscustomstyles': '', '$OpzAppLauncher': '', '$OpzDecimalInclude': '', '$OpzFrameLessDCScripts': '',
         '$OpzHarnessInlineScriptsEnd': '', '$OpzHarnessInlineScriptsStart': '', '$OpzPegaCompositeGadgetScripts': '',
         '$OpzRuntimeToolsBar': '', '$Opzpega_ui_harnesscontext': '', '$Ordlincludes': '', '$OxmlDocumentInclude': '',
         '$OForm': '', '$OGridInc': '', '$OHarness': '', '$OpxHarnessContent': '', '$OpxHeaderCell': '',
         '$OpxWorkArea': '', '$OpxWorkAreaContent': '', '$OpyDirtyCheckConfirm': '', '$OCheckbox': '', '$OLGBundle': '',
         '$OLayoutGroup': '', '$OListView_FilterPanel_Btns': '', '$OListView_header': '', '$OMicroDynamicContainer': '',
         '$OPegaSocial': '', '$ORepeatingGrid': '', '$OpxGrid': '', '$OpxGridBody': '', '$OpxGridDataCell': '',
         '$OpxGridDataRow': '', '$OpxGridHeaderCell': '', '$OpxGridHeaderRow': '', '$OpxMicroDynamicContainer': '',
         '$OpxTextArea': '', '$OpxWorkAreaHeader': '', '$Opycosmoscustomscripts': '', '$OpzLocalActionScript': '',
         '$OpzMicroDynamicContainerScripts': '', '$OpzTextIncludes': '', '$Opzcosmosuiscripts': '',
         '$Opzpega_control_attachcontent': '', '$OpxRadioButtons': '', '$OlfsInclude': '', '$OpxCheckbox': '',
         '$OpxAutoComplete': '', '$OpzAutoCompleteAGIncludes': '', '$OListViewIncludes': '',
         '$OpzRadiogroupIncludes': '', 'PreActivitiesList': '', 'UITemplatingStatus': 'N',
         'StreamClass': 'Rule-HTML-Section', 'bClientValidation': 'true', 'ReadOnly': '0', 'StreamName': 'SelectUser',
         'RenderSingle': 'InitialRender_EXPANDEDSubSectionSelectUser5_pyApproverName', 'AC_PropPage': 'pyWorkPage',
         'BaseReference': 'pyWorkPage', 'inStandardsMode': 'true', 'pzHarnessID': 'HID910FB64868A38C3F75F0EB6A57FD50A3',
         'PreActivity': '', 'PreDataTransform': ''}

        # response = requests.post(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        #     data=data,
        # )
        response = await self.request(
            request_type='POST',
            endpoint='DCSPA_YardCoordinator',
            params=params,
            data=data
        )

    async def step13(self):
        params = {
            'pzTransactionId': 'cf866f2da0f074f10d5f79d02cb3810f',
            'pzFromFrame': 'pyWorkPage',
            'pzPrimaryPageName': 'pyWorkPage',
            'AJAXTrackID': '5',
        }

        data = {
        '$PpyWorkPage$pPriority': 'false', '$PpyWorkPage$ppyApproverName': 'CLEMENTE, ELOY',
         '$PpyWorkPage$ppyAssignedToOperator': '222795', '$PpyWorkPage$ppyWorkListText1': 'CLEMENTE, ELOY',
         'pzuiactionzzz': 'CXt0cn17RENTUEFfWWFyZENvb3JkaW5hdG9yfTAyY2U1NTc1ODg3NDY1ZWY4YjVmZWE5NTU3MzQ0MTc2MTU3Y2RjYmQwMDU3NTdhZjJlNzJhMTUxMjQ3N2YxNGYxMzIzMWVjNmNjZjkyNWY3ZTI4MGUwODFlZjA0ODBlZGM0NzI0NjFmYjIzZWZjYTEzMjliNzNhYjgyMjM1NTA3ZTk1ZTk5ZGQ2MmNkNGM5ZDc2ZTVmMWQ3ZTg2ZDdkNmQ%3D*',
         'PreActivitiesList': '', 'sectionParam': '', 'ActivityParams': '=',
         '$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType': 'WORK', '$OCompositeGadget': '',
         '$OControlMenu': '', '$ODesktopWrapperInclude': '', '$ODeterminePortalTop': '',
         '$ODynamicContainerFrameLess': '', '$ODynamicLayout': '', '$ODynamicLayoutCell': '',
         '$OEvalDOMScripts_Include': '', '$OGapIdentifier': '', '$OHarnessStaticJSEnd': '',
         '$OHarnessStaticJSStart': '', '$OHarnessStaticScriptsClientValidation': '',
         '$OHarnessStaticScriptsExprCal': '', '$OLaunchFlow': '', '$OMenuBar': '', '$OMenuBarOld': '',
         '$OMobileAppNotify': '', '$OOperatorPresenceStatusScripts': '', '$OPMCPortalStaticScripts': '',
         '$ORepeatingDynamicLayout': '', '$OSessionUser': '', '$OSurveyStaticScripts': '', '$OWorkformStyles': '',
         '$Ocosmoslocale': '', '$OmenubarInclude': '', '$OpxButton': '', '$OpxDisplayText': '', '$OpxDropdown': '',
         '$OpxDynamicContainer': '', '$OpxHidden': '', '$OpxIcon': '', '$OpxLayoutContainer': '',
         '$OpxLayoutHeader': '', '$OpxLink': '', '$OpxMenu': '', '$OpxNonTemplate': '', '$OpxSection': '',
         '$OpxTextInput': '', '$OpxVisible': '', '$OpyWorkFormStandardEnd': '', '$OpyWorkFormStandardStart': '',
         '$Opycosmoscustomstyles': '', '$OpzAppLauncher': '', '$OpzDecimalInclude': '', '$OpzFrameLessDCScripts': '',
         '$OpzHarnessInlineScriptsEnd': '', '$OpzHarnessInlineScriptsStart': '', '$OpzPegaCompositeGadgetScripts': '',
         '$OpzRuntimeToolsBar': '', '$Opzpega_ui_harnesscontext': '', '$Ordlincludes': '', '$OxmlDocumentInclude': '',
         '$OForm': '', '$OGridInc': '', '$OHarness': '', '$OpxHarnessContent': '', '$OpxHeaderCell': '',
         '$OpxWorkArea': '', '$OpxWorkAreaContent': '', '$OpyDirtyCheckConfirm': '', '$OCheckbox': '', '$OLGBundle': '',
         '$OLayoutGroup': '', '$OListView_FilterPanel_Btns': '', '$OListView_header': '', '$OMicroDynamicContainer': '',
         '$OPegaSocial': '', '$ORepeatingGrid': '', '$OpxGrid': '', '$OpxGridBody': '', '$OpxGridDataCell': '',
         '$OpxGridDataRow': '', '$OpxGridHeaderCell': '', '$OpxGridHeaderRow': '', '$OpxMicroDynamicContainer': '',
         '$OpxTextArea': '', '$OpxWorkAreaHeader': '', '$Opycosmoscustomscripts': '', '$OpzLocalActionScript': '',
         '$OpzMicroDynamicContainerScripts': '', '$OpzTextIncludes': '', '$Opzcosmosuiscripts': '',
         '$Opzpega_control_attachcontent': '', '$OpxRadioButtons': '', '$OlfsInclude': '', '$OpxCheckbox': '',
         '$OpxAutoComplete': '', '$OpzAutoCompleteAGIncludes': '', '$OListViewIncludes': '',
         '$OpzRadiogroupIncludes': '', 'pyEncodedParameters': 'true', 'pzKeepPageMessages': 'false',
         'strPHarnessClass': 'ESTES-OPS-YardMgmt-Work-Task', 'strPHarnessPurpose': 'Review', 'UITemplatingStatus': 'Y',
         'StreamName': 'SelectUser', 'BaseReference': 'pyWorkPage', 'bClientValidation': 'true', 'FormError': 'NONE',
         'pyCustomError': 'pyCaseErrorSection', 'UsingPage': 'true', 'HeaderButtonSectionName': '-1',
         'PagesToRemove': '', 'pzHarnessID': 'HID910FB64868A38C3F75F0EB6A57FD50A3', 'inStandardsMode': 'true'}

        # response = requests.post(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        #     data=data,
        # )
        response = await self.request(
            request_type='POST',
            endpoint='DCSPA_YardCoordinator',
            params=params,
            data=data
        )

    async def step14(self):
        params = {
            'pzTransactionId': 'cf866f2da0f074f10d5f79d02cb3810f',
            'pzFromFrame': 'pyWorkPage',
            'pzPrimaryPageName': 'pyWorkPage',
            'AJAXTrackID': '5',
        }

        data = {
            'pzuiactionzzz': 'CXt0cn17RENTUEFfWWFyZENvb3JkaW5hdG9yfWM2YmJmOGQ1OTE5ODkzYzVkNjJiNTMzNWQ5YWNiYzgyODU2NDljNzMxYzRkMjViMWQwMmNjYTJhZjQ1NDJkZTM0OGE2MzhhNzZlY2MyZmNlZWVkYTc2YzEwMTM2MWE5YTc4Mjg3YzQxN2I1ZjdmMTRhMTI0NzQzZDM0MTQ0OTA1YWEyOGI1MDIxNDhkNzY3MzNjODc1NGEwM2U5Nzk5NGRiOGY3NDBjYjU2NWNmODcwYzFlMTlkMzEwOWZmMDRkN2UwMmEwYjI3MzcyY2RiOWFlMDE4ZGYyMWViYWEyY2M1ZmY5NzZhZmQ4MGI5Y2I1NTlmOGVlNGUxNzFjMTg1MzU=*=',
            '$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType': 'WORK', '$OCompositeGadget': '',
            '$OControlMenu': '', '$ODesktopWrapperInclude': '', '$ODeterminePortalTop': '',
            '$ODynamicContainerFrameLess': '', '$ODynamicLayout': '', '$ODynamicLayoutCell': '',
            '$OEvalDOMScripts_Include': '', '$OGapIdentifier': '', '$OHarnessStaticJSEnd': '',
            '$OHarnessStaticJSStart': '', '$OHarnessStaticScriptsClientValidation': '',
            '$OHarnessStaticScriptsExprCal': '', '$OLaunchFlow': '', '$OMenuBar': '', '$OMenuBarOld': '',
            '$OMobileAppNotify': '', '$OOperatorPresenceStatusScripts': '', '$OPMCPortalStaticScripts': '',
            '$ORepeatingDynamicLayout': '', '$OSessionUser': '', '$OSurveyStaticScripts': '', '$OWorkformStyles': '',
            '$Ocosmoslocale': '', '$OmenubarInclude': '', '$OpxButton': '', '$OpxDisplayText': '', '$OpxDropdown': '',
            '$OpxDynamicContainer': '', '$OpxHidden': '', '$OpxIcon': '', '$OpxLayoutContainer': '',
            '$OpxLayoutHeader': '', '$OpxLink': '', '$OpxMenu': '', '$OpxNonTemplate': '', '$OpxSection': '',
            '$OpxTextInput': '', '$OpxVisible': '', '$OpyWorkFormStandardEnd': '', '$OpyWorkFormStandardStart': '',
            '$Opycosmoscustomstyles': '', '$OpzAppLauncher': '', '$OpzDecimalInclude': '', '$OpzFrameLessDCScripts': '',
            '$OpzHarnessInlineScriptsEnd': '', '$OpzHarnessInlineScriptsStart': '',
            '$OpzPegaCompositeGadgetScripts': '', '$OpzRuntimeToolsBar': '', '$Opzpega_ui_harnesscontext': '',
            '$Ordlincludes': '', '$OxmlDocumentInclude': '', '$OForm': '', '$OGridInc': '', '$OHarness': '',
            '$OpxHarnessContent': '', '$OpxHeaderCell': '', '$OpxWorkArea': '', '$OpxWorkAreaContent': '',
            '$OpyDirtyCheckConfirm': '', '$OCheckbox': '', '$OLGBundle': '', '$OLayoutGroup': '',
            '$OListView_FilterPanel_Btns': '', '$OListView_header': '', '$OMicroDynamicContainer': '',
            '$OPegaSocial': '', '$ORepeatingGrid': '', '$OpxGrid': '', '$OpxGridBody': '', '$OpxGridDataCell': '',
            '$OpxGridDataRow': '', '$OpxGridHeaderCell': '', '$OpxGridHeaderRow': '', '$OpxMicroDynamicContainer': '',
            '$OpxTextArea': '', '$OpxWorkAreaHeader': '', '$Opycosmoscustomscripts': '', '$OpzLocalActionScript': '',
            '$OpzMicroDynamicContainerScripts': '', '$OpzTextIncludes': '', '$Opzcosmosuiscripts': '',
            '$Opzpega_control_attachcontent': '', '$OpxRadioButtons': '', '$OlfsInclude': '', '$OpxCheckbox': '',
            '$OpxAutoComplete': '', '$OpzAutoCompleteAGIncludes': '', '$OListViewIncludes': '',
            '$OpzRadiogroupIncludes': '', 'UITemplatingStatus': 'N', 'inStandardsMode': 'true',
            'pzHarnessID': 'HID910FB64868A38C3F75F0EB6A57FD50A3'}

        # response = requests.post(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        #     data=data,
        # )
        response = await self.request(
            request_type='POST',
            endpoint='DCSPA_YardCoordinator',
            params=params,
            data=data
        )

    async def step15(self):
        params = {
            'pzTransactionId': '079b747f463ab5a7cbbe2be6079d504e',
            'pzFromFrame': 'pyWorkPage',
            'pzPrimaryPageName': 'pyWorkPage',
            'AJAXTrackID': '5',
        }

        data = {
        '$PpyWorkPage$pMetaData$pIsPickupDoorSelected': 'false', '$PpyWorkPage$pMetaData$pDoorNumber': '99',
         '$PpyWorkPage$pMetaData$pIsPickUpZoneSelected': 'false', '$PpyWorkPage$pMetaData$pIsDoorSelected': 'false',
         '$PpyWorkPage$pMetaData$pDropDoor': '', '$PpyWorkPage$pMetaData$pIsZoneSelected': 'false',
         '$PpyWorkPage$pPriority': 'false', '$PpyWorkPage$ppyApproverName': 'CLEMENTE, ELOY',
         '$PpyWorkPage$ppyAssignedToOperator': '222795', '$PpyWorkPage$ppyWorkListText1': 'CLEMENTE, ELOY',
         'EXPANDEDLGLayoutGroupCaseSummaryS2': '3', 'LGTypeLGLayoutGroupCaseSummaryS2': 'tab',
         '$PpyWorkPage$pMetaData$pPMZoneTrailer': '', '$PpyWorkPage$pMetaData$pZoneTrailer': '',
         '$PpyWorkPage$pMetaData$ppyDescription': 'test',
         'pzuiactionzzz': 'CXt0cn17RENTUEFfWWFyZENvb3JkaW5hdG9yfTAyY2U1NTc1ODg3NDY1ZWY4YjVmZWE5NTU3MzQ0MTc2MTU3Y2RjYmQwMDU3NTdhZjJlNzJhMTUxMjQ3N2YxNGYxMzIzMWVjNmNjZjkyNWY3ZTI4MGUwODFlZjA0ODBlZGI3ZTc5NzNmZjQyNDY5Mjg5NmUyNjhlMGU3ZjUxZTRk*',
         'PreActivitiesList': '', 'ActivityParams': '=',
         '$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType': 'WORK', '$OCompositeGadget': '',
         '$OControlMenu': '', '$ODesktopWrapperInclude': '', '$ODeterminePortalTop': '',
         '$ODynamicContainerFrameLess': '', '$ODynamicLayout': '', '$ODynamicLayoutCell': '',
         '$OEvalDOMScripts_Include': '', '$OGapIdentifier': '', '$OHarnessStaticJSEnd': '',
         '$OHarnessStaticJSStart': '', '$OHarnessStaticScriptsClientValidation': '',
         '$OHarnessStaticScriptsExprCal': '', '$OLaunchFlow': '', '$OMenuBar': '', '$OMenuBarOld': '',
         '$OMobileAppNotify': '', '$OOperatorPresenceStatusScripts': '', '$OPMCPortalStaticScripts': '',
         '$ORepeatingDynamicLayout': '', '$OSessionUser': '', '$OSurveyStaticScripts': '', '$OWorkformStyles': '',
         '$Ocosmoslocale': '', '$OmenubarInclude': '', '$OpxButton': '', '$OpxDisplayText': '', '$OpxDropdown': '',
         '$OpxDynamicContainer': '', '$OpxHidden': '', '$OpxIcon': '', '$OpxLayoutContainer': '',
         '$OpxLayoutHeader': '', '$OpxLink': '', '$OpxMenu': '', '$OpxNonTemplate': '', '$OpxSection': '',
         '$OpxTextInput': '', '$OpxVisible': '', '$OpyWorkFormStandardEnd': '', '$OpyWorkFormStandardStart': '',
         '$Opycosmoscustomstyles': '', '$OpzAppLauncher': '', '$OpzDecimalInclude': '', '$OpzFrameLessDCScripts': '',
         '$OpzHarnessInlineScriptsEnd': '', '$OpzHarnessInlineScriptsStart': '', '$OpzPegaCompositeGadgetScripts': '',
         '$OpzRuntimeToolsBar': '', '$Opzpega_ui_harnesscontext': '', '$Ordlincludes': '', '$OxmlDocumentInclude': '',
         '$OForm': '', '$OGridInc': '', '$OHarness': '', '$OpxHarnessContent': '', '$OpxHeaderCell': '',
         '$OpxWorkArea': '', '$OpxWorkAreaContent': '', '$OpyDirtyCheckConfirm': '', '$OCheckbox': '', '$OLGBundle': '',
         '$OLayoutGroup': '', '$OListView_FilterPanel_Btns': '', '$OListView_header': '', '$OMicroDynamicContainer': '',
         '$OPegaSocial': '', '$ORepeatingGrid': '', '$OpxGrid': '', '$OpxGridBody': '', '$OpxGridDataCell': '',
         '$OpxGridDataRow': '', '$OpxGridHeaderCell': '', '$OpxGridHeaderRow': '', '$OpxMicroDynamicContainer': '',
         '$OpxTextArea': '', '$OpxWorkAreaHeader': '', '$Opycosmoscustomscripts': '', '$OpzLocalActionScript': '',
         '$OpzMicroDynamicContainerScripts': '', '$OpzTextIncludes': '', '$Opzcosmosuiscripts': '',
         '$Opzpega_control_attachcontent': '', '$OpxRadioButtons': '', '$OlfsInclude': '', '$OpxCheckbox': '',
         '$OpxAutoComplete': '', '$OpzAutoCompleteAGIncludes': '', '$OListViewIncludes': '',
         '$OpzRadiogroupIncludes': '', 'PreActivityContextPageList': '$NULL$', 'pzKeepPageMessages': 'false',
         'strPHarnessClass': 'ESTES-OPS-YardMgmt-Work-Task', 'strPHarnessPurpose': 'Review', 'BaseReference': '',
         'StreamList': 'CaseSummary|Rule-HTML-Section||||Y|SID1740317168342|:', 'bClientValidation': 'true',
         'FormError': 'NONE', 'pyCustomError': 'pyCaseErrorSection', 'HeaderButtonSectionName': '-1', 'ReadOnly': '-1',
         'PagesToRemove': 'GridMetadata_1740317168736', 'pzHarnessID': 'HID910FB64868A38C3F75F0EB6A57FD50A3',
         'inStandardsMode': 'true'}

        # response = requests.post(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        #     data=data,
        # )
        response = await self.request(
            request_type='POST',
            endpoint='DCSPA_YardCoordinator',
            params=params,
            data=data
        )

    async def step16(self):
        params = {
            'pzTransactionId': '079b747f463ab5a7cbbe2be6079d504e',
            'pzFromFrame': 'pyWorkPage',
            'pzPrimaryPageName': 'pyWorkPage',
            'AJAXTrackID': '5',
        }

        data = {
        'pyActivity': 'pzRunActionWrapper',
         'strJSON': '{"pyIsCategorizationEnabled":"true","pyIsRowHeightEnabled":"true","pyIsColumnTogglerEnabled":"false","pyIsRefreshListEnabled":"false","pyIsPersonalizationEnabled":"false","pySectionName":"pyCaseHistoryContent","pySectionClass":"Work-","pzCellMethodName":"generateGridCellModes_2","pyRowVisibleCondition":"","pxFilterConditionId":"60665cc4b0c652fde04b6998c74afec9f77cbe70_47","pyResultsClass":"History-Work-","pyIsSearchEnabled":"false","pyPassCurrentParamPage":"false","pxDataSrcId":"60665cc4b0c652fde04b6998c74afec9f77cbe70_46","pyID":1740317179386,"pyPageList":"D_pyWorkHistory_pa636268583143257pz.pxResults","isFilteringEnabled":"true","isSortingEnabled":"true","pzCTMethodName":"gridTemplatePartial_2","pyNoOfColumnsCategorized":0,"pyIsTableCategorized":"false","pxObjClass":"Pega-UI-Component-Grid-Filter","pyColumns":[{"pyLabel":"Time","pyPropertyName":".pxTimeCreated","pyDataType":"DateTime","pyFilterType":"true","pyColumnSorting":"true","pyCellWidth":"305px","pyInitialOrder":1,"pyContentType":"FIELD","pyFilterPanelSection":"pzFilterPanelDateTime","pyMobileFilterPanelSection":"pzMobileFilterPanelDateTime","pyColumnVisibility":"AV","pyOrder":1,"pyShow":true,"pxObjClass":"Embed-FilterColumn"},{"pyLabel":"Description","pyPropertyName":".pyMessageKey","pyDataType":"Text","pyFilterType":"true","pyColumnSorting":"true","pyCellWidth":"802px","pyInitialOrder":2,"pyContentType":"FIELD","pyFilterPanelSection":"pzFilterPanelText","pyMobileFilterPanelSection":"pzMobileFilterPanelText","pyColumnVisibility":"IV","pyOrder":2,"pyShow":true,"pxObjClass":"Embed-FilterColumn"},{"pyLabel":"Performed by","pyPropertyName":".pyPerformer","pyDataType":"Text","pyFilterType":"true","pyColumnSorting":"true","pyCellWidth":"174px","pyInitialOrder":3,"pyContentType":"FIELD","pyFilterPanelSection":"pzFilterPanelText","pyMobileFilterPanelSection":"pzMobileFilterPanelText","pyColumnVisibility":"AV","pyOrder":3,"pyShow":true,"pxObjClass":"Embed-FilterColumn"}],"pyIsModified":"false"}',
         '$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType': 'WORK', '$OCompositeGadget': '',
         '$OControlMenu': '', '$ODesktopWrapperInclude': '', '$ODeterminePortalTop': '',
         '$ODynamicContainerFrameLess': '', '$ODynamicLayout': '', '$ODynamicLayoutCell': '',
         '$OEvalDOMScripts_Include': '', '$OGapIdentifier': '', '$OHarnessStaticJSEnd': '',
         '$OHarnessStaticJSStart': '', '$OHarnessStaticScriptsClientValidation': '',
         '$OHarnessStaticScriptsExprCal': '', '$OLaunchFlow': '', '$OMenuBar': '', '$OMenuBarOld': '',
         '$OMobileAppNotify': '', '$OOperatorPresenceStatusScripts': '', '$OPMCPortalStaticScripts': '',
         '$ORepeatingDynamicLayout': '', '$OSessionUser': '', '$OSurveyStaticScripts': '', '$OWorkformStyles': '',
         '$Ocosmoslocale': '', '$OmenubarInclude': '', '$OpxButton': '', '$OpxDisplayText': '', '$OpxDropdown': '',
         '$OpxDynamicContainer': '', '$OpxHidden': '', '$OpxIcon': '', '$OpxLayoutContainer': '',
         '$OpxLayoutHeader': '', '$OpxLink': '', '$OpxMenu': '', '$OpxNonTemplate': '', '$OpxSection': '',
         '$OpxTextInput': '', '$OpxVisible': '', '$OpyWorkFormStandardEnd': '', '$OpyWorkFormStandardStart': '',
         '$Opycosmoscustomstyles': '', '$OpzAppLauncher': '', '$OpzDecimalInclude': '', '$OpzFrameLessDCScripts': '',
         '$OpzHarnessInlineScriptsEnd': '', '$OpzHarnessInlineScriptsStart': '', '$OpzPegaCompositeGadgetScripts': '',
         '$OpzRuntimeToolsBar': '', '$Opzpega_ui_harnesscontext': '', '$Ordlincludes': '', '$OxmlDocumentInclude': '',
         '$OForm': '', '$OGridInc': '', '$OHarness': '', '$OpxHarnessContent': '', '$OpxHeaderCell': '',
         '$OpxWorkArea': '', '$OpxWorkAreaContent': '', '$OpyDirtyCheckConfirm': '', '$OCheckbox': '', '$OLGBundle': '',
         '$OLayoutGroup': '', '$OListView_FilterPanel_Btns': '', '$OListView_header': '', '$OMicroDynamicContainer': '',
         '$OPegaSocial': '', '$ORepeatingGrid': '', '$OpxGrid': '', '$OpxGridBody': '', '$OpxGridDataCell': '',
         '$OpxGridDataRow': '', '$OpxGridHeaderCell': '', '$OpxGridHeaderRow': '', '$OpxMicroDynamicContainer': '',
         '$OpxTextArea': '', '$OpxWorkAreaHeader': '', '$Opycosmoscustomscripts': '', '$OpzLocalActionScript': '',
         '$OpzMicroDynamicContainerScripts': '', '$OpzTextIncludes': '', '$Opzcosmosuiscripts': '',
         '$Opzpega_control_attachcontent': '', '$OpxRadioButtons': '', '$OlfsInclude': '', '$OpxCheckbox': '',
         '$OpxAutoComplete': '', '$OpzAutoCompleteAGIncludes': '', '$OListViewIncludes': '',
         '$OpzRadiogroupIncludes': '', 'instanceId': '1740317179386', 'pzKeepPageMessages': 'true',
         'UITemplatingStatus': 'N', 'inStandardsMode': 'true', 'pzHarnessID': 'HID910FB64868A38C3F75F0EB6A57FD50A3',
         'pzActivity': 'pzBuildFilterIcon', 'skipReturnResponse': 'true', 'pySubAction': 'runAct'}

        # response = requests.post(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        #     data=data,
        # )
        response = await self.request(
            request_type='POST',
            endpoint='DCSPA_YardCoordinator',
            params=params,
            data=data
        )

    async def step17(self):
        params = {
            'pzTransactionId': '079b747f463ab5a7cbbe2be6079d504e',
            'pzFromFrame': 'pyWorkPage',
            'pzPrimaryPageName': 'pyWorkPage',
            'AJAXTrackID': '5',
        }

        data = {
        'pyActivity': 'ReloadSection', '$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType': 'WORK',
         '$OCompositeGadget': '', '$OControlMenu': '', '$ODesktopWrapperInclude': '', '$ODeterminePortalTop': '',
         '$ODynamicContainerFrameLess': '', '$ODynamicLayout': '', '$ODynamicLayoutCell': '',
         '$OEvalDOMScripts_Include': '', '$OGapIdentifier': '', '$OHarnessStaticJSEnd': '',
         '$OHarnessStaticJSStart': '', '$OHarnessStaticScriptsClientValidation': '',
         '$OHarnessStaticScriptsExprCal': '', '$OLaunchFlow': '', '$OMenuBar': '', '$OMenuBarOld': '',
         '$OMobileAppNotify': '', '$OOperatorPresenceStatusScripts': '', '$OPMCPortalStaticScripts': '',
         '$ORepeatingDynamicLayout': '', '$OSessionUser': '', '$OSurveyStaticScripts': '', '$OWorkformStyles': '',
         '$Ocosmoslocale': '', '$OmenubarInclude': '', '$OpxButton': '', '$OpxDisplayText': '', '$OpxDropdown': '',
         '$OpxDynamicContainer': '', '$OpxHidden': '', '$OpxIcon': '', '$OpxLayoutContainer': '',
         '$OpxLayoutHeader': '', '$OpxLink': '', '$OpxMenu': '', '$OpxNonTemplate': '', '$OpxSection': '',
         '$OpxTextInput': '', '$OpxVisible': '', '$OpyWorkFormStandardEnd': '', '$OpyWorkFormStandardStart': '',
         '$Opycosmoscustomstyles': '', '$OpzAppLauncher': '', '$OpzDecimalInclude': '', '$OpzFrameLessDCScripts': '',
         '$OpzHarnessInlineScriptsEnd': '', '$OpzHarnessInlineScriptsStart': '', '$OpzPegaCompositeGadgetScripts': '',
         '$OpzRuntimeToolsBar': '', '$Opzpega_ui_harnesscontext': '', '$Ordlincludes': '', '$OxmlDocumentInclude': '',
         '$OForm': '', '$OGridInc': '', '$OHarness': '', '$OpxHarnessContent': '', '$OpxHeaderCell': '',
         '$OpxWorkArea': '', '$OpxWorkAreaContent': '', '$OpyDirtyCheckConfirm': '', '$OCheckbox': '', '$OLGBundle': '',
         '$OLayoutGroup': '', '$OListView_FilterPanel_Btns': '', '$OListView_header': '', '$OMicroDynamicContainer': '',
         '$OPegaSocial': '', '$ORepeatingGrid': '', '$OpxGrid': '', '$OpxGridBody': '', '$OpxGridDataCell': '',
         '$OpxGridDataRow': '', '$OpxGridHeaderCell': '', '$OpxGridHeaderRow': '', '$OpxMicroDynamicContainer': '',
         '$OpxTextArea': '', '$OpxWorkAreaHeader': '', '$Opycosmoscustomscripts': '', '$OpzLocalActionScript': '',
         '$OpzMicroDynamicContainerScripts': '', '$OpzTextIncludes': '', '$Opzcosmosuiscripts': '',
         '$Opzpega_control_attachcontent': '', '$OpxRadioButtons': '', '$OlfsInclude': '', '$OpxCheckbox': '',
         '$OpxAutoComplete': '', '$OpzAutoCompleteAGIncludes': '', '$OListViewIncludes': '',
         '$OpzRadiogroupIncludes': '', 'PreActivitiesList': '', 'ReadOnly': '-1', 'StreamName': 'CaseSummary',
         'StreamClass': 'Rule-HTML-Section', 'strPHarnessClass': 'ESTES-OPS-YardMgmt-Work-Task',
         'strPHarnessPurpose': 'Review', 'BaseReference': '', 'bClientValidation': 'true', 'FieldError': '',
         'FormError': 'NONE', 'pyCustomError': 'pyCaseErrorSection', 'pzKeepPageMessages': 'true',
         'pyCallStreamMethod': 'pzLayoutContainer_2', 'pyLayoutMethodName': 'pzLayoutContainer_2',
         'UITemplatingStatus': 'Y', 'inStandardsMode': 'true', 'pzHarnessID': 'HID910FB64868A38C3F75F0EB6A57FD50A3',
         'PreActivity': '', 'PreDataTransform': ''}

        # response = requests.post(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        #     data=data,
        # )
        response = await self.request(
            request_type='GET',
            endpoint='DCSPA_YardCoordinator',
            params=params,
        )

    async def step18(self):
        params = {
            'pyActivity': 'DoClose',
            'pzFromFrame': 'pyWorkPage',
            'pzPrimaryPageName': 'pyWorkPage',
            'pyRemCtlExpProp': 'true',
            'pzHarnessID': 'HID88142B62BC212424E4D40CD6829A915D',
            'AJAXTrackID': '5',
            'retainLock': 'false',
            'dcCleanup': 'true',
        }

        # response = requests.get(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        # )
        response = await self.request(
            request_type='GET',
            endpoint='DCSPA_YardCoordinator',
            params=params,
        )

    async def step19(self):
        params = {
            'pzTransactionId': 'fa451240bc89c7e4fe7671b2cf14c4fe',
        }

        data = {
        'isDCSPA': 'true', 'AJAXTrackID': '2',
         '$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType': 'HARNESS', '$OCompositeGadget': '',
         '$OControlMenu': '', '$ODesktopWrapperInclude': '', '$ODeterminePortalTop': '',
         '$ODynamicContainerFrameLess': '', '$ODynamicLayout': '', '$ODynamicLayoutCell': '',
         '$OEvalDOMScripts_Include': '', '$OGapIdentifier': '', '$OHarnessStaticJSEnd': '',
         '$OHarnessStaticJSStart': '', '$OHarnessStaticScriptsClientValidation': '',
         '$OHarnessStaticScriptsExprCal': '', '$OLaunchFlow': '', '$OMenuBar': '', '$OMenuBarOld': '',
         '$OMobileAppNotify': '', '$OOperatorPresenceStatusScripts': '', '$OPMCPortalStaticScripts': '',
         '$ORepeatingDynamicLayout': '', '$OSessionUser': '', '$OSurveyStaticScripts': '', '$OWorkformStyles': '',
         '$Ocosmoslocale': '', '$OmenubarInclude': '', '$OpxButton': '', '$OpxDisplayText': '', '$OpxDropdown': '',
         '$OpxDynamicContainer': '', '$OpxHidden': '', '$OpxIcon': '', '$OpxLayoutContainer': '',
         '$OpxLayoutHeader': '', '$OpxLink': '', '$OpxMenu': '', '$OpxNonTemplate': '', '$OpxSection': '',
         '$OpxTextInput': '', '$OpxVisible': '', '$OpyWorkFormStandardEnd': '', '$OpyWorkFormStandardStart': '',
         '$Opycosmoscustomstyles': '', '$OpzAppLauncher': '', '$OpzDecimalInclude': '', '$OpzFrameLessDCScripts': '',
         '$OpzHarnessInlineScriptsEnd': '', '$OpzHarnessInlineScriptsStart': '', '$OpzPegaCompositeGadgetScripts': '',
         '$OpzRuntimeToolsBar': '', '$Opzpega_ui_harnesscontext': '', '$Ordlincludes': '', '$OxmlDocumentInclude': '',
         '$OForm': '', '$OGridInc': '', '$OHarness': '', '$OpxHarnessContent': '', '$OpxHeaderCell': '',
         '$OpxWorkArea': '', '$OpxWorkAreaContent': '', '$OpyDirtyCheckConfirm': '', '$OCheckbox': '', '$OLGBundle': '',
         '$OLayoutGroup': '', '$OListView_FilterPanel_Btns': '', '$OListView_header': '', '$OMicroDynamicContainer': '',
         '$OPegaSocial': '', '$ORepeatingGrid': '', '$OpxGrid': '', '$OpxGridBody': '', '$OpxGridDataCell': '',
         '$OpxGridDataRow': '', '$OpxGridHeaderCell': '', '$OpxGridHeaderRow': '', '$OpxMicroDynamicContainer': '',
         '$OpxTextArea': '', '$OpxWorkAreaHeader': '', '$Opycosmoscustomscripts': '', '$OpzLocalActionScript': '',
         '$OpzMicroDynamicContainerScripts': '', '$OpzTextIncludes': '', '$Opzcosmosuiscripts': '',
         '$Opzpega_control_attachcontent': '', '$OpxRadioButtons': '', '$OlfsInclude': '', '$OpxCheckbox': '',
         '$OpxAutoComplete': '', '$OpzAutoCompleteAGIncludes': '', '$OListViewIncludes': '',
         '$OpzRadiogroupIncludes': '', 'isURLReady': 'true', 'api': 'activate', 'UITemplatingStatus': 'Y',
         'inStandardsMode': 'true', 'pzHarnessID': 'HIDAFE941E341451946936AC79C109819DF'
        }

        # response = requests.post(
        #     'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!STANDARD',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        #     data=data,
        # )
        response = await self.request(
            request_type='POST',
            endpoint='STANDARD',
            params=params,
            data=data
        )

    async def request(self, request_type: str, endpoint: str, params, data):
        response = None

        if data:
            if request_type.upper() == 'POST':
                response = self.async_client.get(
                    url=self.base_url + endpoint,
                    params=params,
                    data=data
                )
            elif request_type.upper() == 'GET':
                response = self.async_client.get(
                    url=self.base_url + endpoint,
                    params=params,
                    data=data
                )
        elif data is None:
            if request_type.upper() == 'POST':
                response = self.async_client.get(
                    url=self.base_url + endpoint,
                    params=params,
                )
            elif request_type.upper() == 'GET':
                response = self.async_client.get(
                    url=self.base_url + endpoint,
                    params=params,
                )
        else:
            raise Exception('Transfer Task request type not supported. [ request type was not a GET or POST ]')

        return response

    async def transfer_task(self):
        await self.get_task()
        await self.step5()
