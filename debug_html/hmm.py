import requests


params = {
    'eventSrcSection': 'Data-Portal.PortalNavigation',
}

data = 'pyActivity=%40baseclass.doUIAction&isDCSPA=true&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OGapIdentifier=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput=&$OpxVisible=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OForm=&$OHarness=&$OLGBundle=&$OLayoutGroup=&$OListView_FilterPanel_Btns=&$OListView_header=&$OMicroDynamicContainer=&$OPegaSocial=&$ORepeatingGrid=&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&$OpxGridHeaderRow=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxMicroDynamicContainer=&$OpxTextArea=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpxWorkAreaHeader=&$OpyDirtyCheckConfirm=&$Opycosmoscustomscripts=&$OpzLocalActionScript=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes=&$Opzcosmosuiscripts=&$Opzpega_control_attachcontent=&$OGridInc=&isSDM=true&action=display&label=Search&className=ESTES-OPS-YardMgmt-UIPages&harnessName=Search_1&contentID=aef46764-46e8-0197-0191-b77251287605&SkipConflictCheck=true&readOnly=false&tabName=Search&replaceCurrent=false&api=display&portalName=YardCoordinator&portalThreadName=STANDARD&tabIndex=1&pzHarnessID=HID9484605AE427292FC7D02AB93F064856&UITemplatingStatus=Y&inStandardsMode=true&eventSrcSection=Data-Portal.PortalNavigation'

response = requests.post(
    'https://ymg.estes-express.com/prweb/app/YardMgmt/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
    params=params,
    data=data,
)


params = {
    'pzTransactionId': '',
    'pzFromFrame': '',
    'pzPrimaryPageName': 'pyDisplayHarness',
    'AJAXTrackID': '1',
}

data = 'pyActivity=ReloadSection&D_SearchResultsPpxResults1colWidthGBL=&D_SearchResultsPpxResults1colWidthGBR=&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=HOME&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OGapIdentifier=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput=&$OpxVisible=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OForm=&$OHarness=&$OLGBundle=&$OLayoutGroup=&$OListView_FilterPanel_Btns=&$OListView_header=&$OMicroDynamicContainer=&$OPegaSocial=&$ORepeatingGrid=&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&$OpxGridHeaderRow=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxMicroDynamicContainer=&$OpxTextArea=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpxWorkAreaHeader=&$OpyDirtyCheckConfirm=&$Opycosmoscustomscripts=&$OpzLocalActionScript=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes=&$Opzcosmosuiscripts=&$Opzpega_control_attachcontent=&$OGridInc=&PreActivitiesList=&StreamName=SearchResults&RenderSingle=EXPANDEDSubSectionSearchResultsB~pzLayout_1&StreamClass=Rule-HTML-Section&bClientValidation=true&PreActivity=pzdoGridAction&ActivityParams=gridAction%3DREFRESHLIST%26BaseReference%3DD_SearchInputs%26isReportDef%3Dfalse&UsingPage=true&BaseReference=D_SearchInputs&ReadOnly=0&Increment=true&UITemplatingStatus=N&inStandardsMode=true&pzHarnessID=HIDD164629B9AB9F925C5FE1B7383B5DCC6&PreDataTransform='

response = requests.post(
    'https://ymg.estes-express.com/prweb/app/YardMgmt/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
    params=params,
    data=data,
)


params = {
    'pzTransactionId': '',
    'pzFromFrame': '',
    'pzPrimaryPageName': 'pyDisplayHarness',
    'AJAXTrackID': '1',
}

data = '$PD_SearchInputs$ppyID=T-34290443&$PD_SearchInputs$pMetaData$pDoorNumber=&$PD_SearchInputs$pMetaData$pTrailerNumber=&$PD_SearchInputs$ppyAssignedOperator=&pzuiactionzzz=CXt0cn17RENTUEFfWWFyZENvb3JkaW5hdG9yfWUyN2FiMDg2NDU2MGJkYTliYjgwNmYyMmZiNjc5Yzg3ZDc2ZWRkMzk0NmU0M2FjZmVjNDdjY2QwODZiNDNmYzAzZGIzZjFjZTg0ZDJjMjA3ZTFmNDc3MzZmNDI0ODZlMDUwNTc3ZTNhYTAzZTc3MjdkMjMxNzczNWVlZDJhN2I2MWU4ZTc3ZDA4NWM3YjE1NDUwM2U3YTg1NTA0Mzc5N2Q%253D*&PreActivitiesList=&sectionParam=&ActivityParams=%3D&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=HOME&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OGapIdentifier=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput=&$OpxVisible=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OForm=&$OHarness=&$OLGBundle=&$OLayoutGroup=&$OListView_FilterPanel_Btns=&$OListView_header=&$OMicroDynamicContainer=&$OPegaSocial=&$ORepeatingGrid=&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&$OpxGridHeaderRow=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxMicroDynamicContainer=&$OpxTextArea=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpxWorkAreaHeader=&$OpyDirtyCheckConfirm=&$Opycosmoscustomscripts=&$OpzLocalActionScript=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes=&$Opzcosmosuiscripts=&$Opzpega_control_attachcontent=&$OGridInc=&pyEncodedParameters=true&pzKeepPageMessages=false&strPHarnessClass=ESTES-OPS-YardMgmt-UIPages&strPHarnessPurpose=Search_1&UITemplatingStatus=Y&StreamName=SearchInputs&BaseReference=D_SearchInputs&bClientValidation=true&UsingPage=true&HeaderButtonSectionName=-1&PagesToRemove=&pzHarnessID=HIDD164629B9AB9F925C5FE1B7383B5DCC6&inStandardsMode=true'

response = requests.post(
    'https://ymg.estes-express.com/prweb/app/YardMgmt/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
    params=params,
    data=data,
)


params = {
    'pzTransactionId': '',
    'pzFromFrame': '',
    'pzPrimaryPageName': 'pyDisplayHarness',
    'AJAXTrackID': '1',
}

data = '$PD_SearchInputs$ppyID=T-34290443&$PD_SearchInputs$pMetaData$pDoorNumber=&$PD_SearchInputs$pMetaData$pTrailerNumber=&$PD_SearchInputs$ppyAssignedOperator=&D_SearchResultsPpxResults1colWidthGBL=&D_SearchResultsPpxResults1colWidthGBR=&pzuiactionzzz=CXt0cn17RENTUEFfWWFyZENvb3JkaW5hdG9yfWUyN2FiMDg2NDU2MGJkYTliYjgwNmYyMmZiNjc5Yzg3ZDc2ZWRkMzk0NmU0M2FjZmVjNDdjY2QwODZiNDNmYzAzZGIzZjFjZTg0ZDJjMjA3ZTFmNDc3MzZmNDI0ODZlMDM3MDk5YmVjZDUyMDZlYjQ3Nzg3ZTMyY2RiZjEyZTMx*&PreActivitiesList=&ActivityParams=%3D&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=HOME&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OGapIdentifier=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput=&$OpxVisible=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OForm=&$OHarness=&$OLGBundle=&$OLayoutGroup=&$OListView_FilterPanel_Btns=&$OListView_header=&$OMicroDynamicContainer=&$OPegaSocial=&$ORepeatingGrid=&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&$OpxGridHeaderRow=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxMicroDynamicContainer=&$OpxTextArea=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpxWorkAreaHeader=&$OpyDirtyCheckConfirm=&$Opycosmoscustomscripts=&$OpzLocalActionScript=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes=&$Opzcosmosuiscripts=&$Opzpega_control_attachcontent=&$OGridInc=&PreActivityContextPageList=%24NULL%24&pzKeepPageMessages=false&strPHarnessClass=ESTES-OPS-YardMgmt-UIPages&strPHarnessPurpose=Search_1&BaseReference=&StreamList=SearchDetails%7CRule-HTML-Section%7C%7C%7C%7CY%7CSID1751309393671%7C%3A&bClientValidation=true&HeaderButtonSectionName=-1&PagesToRemove=&pzHarnessID=HIDD164629B9AB9F925C5FE1B7383B5DCC6&inStandardsMode=true'

response = requests.post(
    'https://ymg.estes-express.com/prweb/app/YardMgmt/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
    params=params,
    data=data,
)


data = 'pyActivity=%40baseclass.doUIAction&isDCSPA=true&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OGapIdentifier=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput=&$OpxVisible=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OForm=&$OHarness=&$OLGBundle=&$OLayoutGroup=&$OListView_FilterPanel_Btns=&$OListView_header=&$OMicroDynamicContainer=&$OPegaSocial=&$ORepeatingGrid=&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&$OpxGridHeaderRow=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxMicroDynamicContainer=&$OpxTextArea=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpxWorkAreaHeader=&$OpyDirtyCheckConfirm=&$Opycosmoscustomscripts=&$OpzLocalActionScript=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes=&$Opzcosmosuiscripts=&$Opzpega_control_attachcontent=&$OGridInc=&isSDM=true&action=openWorkByHandle&key=ESTES-OPS-YARDMGMT-WORK%20T-34290443&SkipConflictCheck=false&reload=false&api=openWorkByHandle&contentID=b418f2e8-decd-a178-8738-a3cb0dd10b33&portalName=YardCoordinator&portalThreadName=STANDARD&tabIndex=1&pzHarnessID=HIDD164629B9AB9F925C5FE1B7383B5DCC6&UITemplatingStatus=Y&inStandardsMode=true'

response = requests.post(
    'https://ymg.estes-express.com/prweb/app/YardMgmt/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
    data=data,
)


params = {
    'pzTransactionId': 'e14d45d4563e450107b345690f319667',
    'pzFromFrame': 'pyWorkPage',
    'pzPrimaryPageName': 'pyWorkPage',
    'AJAXTrackID': '2',
}

data = 'pyActivity=pzRunActionWrapper&strJSON=%7B%22pyIsCategorizationEnabled%22%3A%22true%22%2C%22pyIsRowHeightEnabled%22%3A%22true%22%2C%22pyIsColumnTogglerEnabled%22%3A%22false%22%2C%22pyIsRefreshListEnabled%22%3A%22false%22%2C%22pyIsPersonalizationEnabled%22%3A%22false%22%2C%22pySectionName%22%3A%22pyCaseHistoryContent%22%2C%22pySectionClass%22%3A%22Work-%22%2C%22pzCellMethodName%22%3A%22generateGridCellModes_2%22%2C%22pyRowVisibleCondition%22%3A%22%22%2C%22pxFilterConditionId%22%3A%2260665cc4b0c652fde04b6998c74afec9f77cbe70_47%22%2C%22pyResultsClass%22%3A%22History-Work-%22%2C%22pyIsSearchEnabled%22%3A%22false%22%2C%22pyPassCurrentParamPage%22%3A%22false%22%2C%22pxDataSrcId%22%3A%2260665cc4b0c652fde04b6998c74afec9f77cbe70_46%22%2C%22pyID%22%3A1751309405115%2C%22pyPageList%22%3A%22D_pyWorkHistory_pa742178962929645pz.pxResults%22%2C%22isFilteringEnabled%22%3A%22true%22%2C%22isSortingEnabled%22%3A%22true%22%2C%22pzCTMethodName%22%3A%22gridTemplatePartial_2%22%2C%22pyNoOfColumnsCategorized%22%3A0%2C%22pyIsTableCategorized%22%3A%22false%22%2C%22pxObjClass%22%3A%22Pega-UI-Component-Grid-Filter%22%2C%22pyColumns%22%3A%5B%7B%22pyLabel%22%3A%22Time%22%2C%22pyPropertyName%22%3A%22.pxTimeCreated%22%2C%22pyDataType%22%3A%22DateTime%22%2C%22pyFilterType%22%3A%22true%22%2C%22pyColumnSorting%22%3A%22true%22%2C%22pyCellWidth%22%3A%22305px%22%2C%22pyInitialOrder%22%3A1%2C%22pyContentType%22%3A%22FIELD%22%2C%22pyFilterPanelSection%22%3A%22pzFilterPanelDateTime%22%2C%22pyMobileFilterPanelSection%22%3A%22pzMobileFilterPanelDateTime%22%2C%22pyColumnVisibility%22%3A%22AV%22%2C%22pyOrder%22%3A1%2C%22pyShow%22%3Atrue%2C%22pxObjClass%22%3A%22Embed-FilterColumn%22%7D%2C%7B%22pyLabel%22%3A%22Description%22%2C%22pyPropertyName%22%3A%22.pyMessageKey%22%2C%22pyDataType%22%3A%22Text%22%2C%22pyFilterType%22%3A%22true%22%2C%22pyColumnSorting%22%3A%22true%22%2C%22pyCellWidth%22%3A%22802px%22%2C%22pyInitialOrder%22%3A2%2C%22pyContentType%22%3A%22FIELD%22%2C%22pyFilterPanelSection%22%3A%22pzFilterPanelText%22%2C%22pyMobileFilterPanelSection%22%3A%22pzMobileFilterPanelText%22%2C%22pyColumnVisibility%22%3A%22IV%22%2C%22pyOrder%22%3A2%2C%22pyShow%22%3Atrue%2C%22pxObjClass%22%3A%22Embed-FilterColumn%22%7D%2C%7B%22pyLabel%22%3A%22Performed%20by%22%2C%22pyPropertyName%22%3A%22.pyPerformer%22%2C%22pyDataType%22%3A%22Text%22%2C%22pyFilterType%22%3A%22true%22%2C%22pyColumnSorting%22%3A%22true%22%2C%22pyCellWidth%22%3A%22174px%22%2C%22pyInitialOrder%22%3A3%2C%22pyContentType%22%3A%22FIELD%22%2C%22pyFilterPanelSection%22%3A%22pzFilterPanelText%22%2C%22pyMobileFilterPanelSection%22%3A%22pzMobileFilterPanelText%22%2C%22pyColumnVisibility%22%3A%22AV%22%2C%22pyOrder%22%3A3%2C%22pyShow%22%3Atrue%2C%22pxObjClass%22%3A%22Embed-FilterColumn%22%7D%5D%2C%22pyIsModified%22%3A%22false%22%7D&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=WORK&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OGapIdentifier=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput=&$OpxVisible=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OForm=&$OHarness=&$OLGBundle=&$OLayoutGroup=&$OListView_FilterPanel_Btns=&$OListView_header=&$OMicroDynamicContainer=&$OPegaSocial=&$ORepeatingGrid=&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&$OpxGridHeaderRow=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxMicroDynamicContainer=&$OpxTextArea=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpxWorkAreaHeader=&$OpyDirtyCheckConfirm=&$Opycosmoscustomscripts=&$OpzLocalActionScript=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes=&$Opzcosmosuiscripts=&$Opzpega_control_attachcontent=&$OGridInc=&instanceId=1751309405115&pzKeepPageMessages=true&UITemplatingStatus=N&inStandardsMode=true&pzHarnessID=HIDEE3EC0D86107D9EB0D6710B8FEEBE621&pzActivity=pzBuildFilterIcon&skipReturnResponse=true&pySubAction=runAct'

response = requests.post(
    'https://ymg.estes-express.com/prweb/app/YardMgmt/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
    params=params,
    data=data,
)


params = {
    'pzTransactionId': 'e14d45d4563e450107b345690f319667',
    'pzFromFrame': 'pyWorkPage',
    'pzPrimaryPageName': 'pyWorkPage',
    'AJAXTrackID': '2',
}

data = 'pyActivity=ReloadSection&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=WORK&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OGapIdentifier=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput=&$OpxVisible=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OForm=&$OHarness=&$OLGBundle=&$OLayoutGroup=&$OListView_FilterPanel_Btns=&$OListView_header=&$OMicroDynamicContainer=&$OPegaSocial=&$ORepeatingGrid=&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&$OpxGridHeaderRow=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxMicroDynamicContainer=&$OpxTextArea=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpxWorkAreaHeader=&$OpyDirtyCheckConfirm=&$Opycosmoscustomscripts=&$OpzLocalActionScript=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes=&$Opzcosmosuiscripts=&$Opzpega_control_attachcontent=&$OGridInc=&PreActivitiesList=&ReadOnly=-1&StreamName=CaseSummary&StreamClass=Rule-HTML-Section&strPHarnessClass=ESTES-OPS-YardMgmt-Work-Task&strPHarnessPurpose=Review&BaseReference=&bClientValidation=true&FieldError=&FormError=NONE&pyCustomError=pyCaseErrorSection&pzKeepPageMessages=true&pyCallStreamMethod=pzLayoutContainer_2&pyLayoutMethodName=pzLayoutContainer_2&UITemplatingStatus=Y&inStandardsMode=true&pzHarnessID=HIDEE3EC0D86107D9EB0D6710B8FEEBE621&PreActivity=&PreDataTransform='

response = requests.post(
    'https://ymg.estes-express.com/prweb/app/YardMgmt/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
    params=params,
    data=data,
)


params = {
    'pzTransactionId': 'e14d45d4563e450107b345690f319667',
    'pzFromFrame': 'pyWorkPage',
    'pzPrimaryPageName': 'pyWorkPage',
    'AJAXTrackID': '2',
}

data = 'pyActivity=ProcessAction&$PpyWorkPage$ppyInternalAssignmentHandle=ASSIGN-INTERNAL%20ESTES-OPS-YARDMGMT-WORK%20T-34290443!PZINTERNALCASEFLOW&HarnessType=Review&Purpose=Review&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=WORK&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OGapIdentifier=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput=&$OpxVisible=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OForm=&$OHarness=&$OLGBundle=&$OLayoutGroup=&$OListView_FilterPanel_Btns=&$OListView_header=&$OMicroDynamicContainer=&$OPegaSocial=&$ORepeatingGrid=&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&$OpxGridHeaderRow=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxMicroDynamicContainer=&$OpxTextArea=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpxWorkAreaHeader=&$OpyDirtyCheckConfirm=&$Opycosmoscustomscripts=&$OpzLocalActionScript=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes=&$Opzcosmosuiscripts=&$Opzpega_control_attachcontent=&$OGridInc=&UITemplatingStatus=Y&NewTaskStatus=DeleteTask&TaskIndex=&StreamType=Rule-HTML-Section&FieldError=&FormError=NONE&pyCustomError=pyCaseErrorSection&bExcludeLegacyJS=true&ModalSection=pzModalTemplate&modalStyle=&IgnoreSectionSubmit=true&bInvokedFromControl=true&BaseReference=&isModalFlowAction=true&bIsModal=true&bIsOverlay=false&StreamClass=Rule-HTML-Section&UITemplatingScriptLoad=true&ActionSection=pzModalTemplate&pzHarnessID=HIDEE3EC0D86107D9EB0D6710B8FEEBE621&inStandardsMode=true'

response = requests.post(
    'https://ymg.estes-express.com/prweb/app/YardMgmt/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
    params=params,
    data=data,
)

params = {
    'pzTransactionId': 'e14d45d4563e450107b345690f319667',
    'pzFromFrame': 'pyWorkPage',
    'pzPrimaryPageName': 'pyWorkPage',
    'AJAXTrackID': '2',
}

data = 'pzuiactionzzz=CXt0cn17RENTUEFfWWFyZENvb3JkaW5hdG9yfWE3NjQ2ZGIwMmQwZTQxNDlkMGE3ZTdjMGZlZmFiMjQ3ODdmODVlYzFmZGZkYmJiZWI2N2U1OTVkZjc4MzM3ZWM3MWViYzU2ODNkMDMzMGE3Y2MxNjgwYjA4MTRjYTlmYjExYWUyNDViZmNmYmUzODdkYzczMjhmMjk5MGI2ODViMTc4ZDE4MGU5NDA1MWIxOWFiZmNiYjZlZGQyNjM1NDgxOWRjNDg3ZDNiZDE2MzViM2ViZTU5NGYyYTFkZTg5M2UwODc3NGY1MjA5MjMzMTBmODNkZDkyZDcwNGM2ZTg5*=&AssignmentID=ESTES-OPS-YARDMGMT-WORK%2520T-34290443&pzActivityParams=AssignmentID&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=WORK&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OGapIdentifier=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput=&$OpxVisible=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OForm=&$OHarness=&$OLGBundle=&$OLayoutGroup=&$OListView_FilterPanel_Btns=&$OListView_header=&$OMicroDynamicContainer=&$OPegaSocial=&$ORepeatingGrid=&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&$OpxGridHeaderRow=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxMicroDynamicContainer=&$OpxTextArea=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpxWorkAreaHeader=&$OpyDirtyCheckConfirm=&$Opycosmoscustomscripts=&$OpzLocalActionScript=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes=&$Opzcosmosuiscripts=&$Opzpega_control_attachcontent=&$OGridInc=&UITemplatingStatus=N&inStandardsMode=true&pzHarnessID=HIDEE3EC0D86107D9EB0D6710B8FEEBE621'

response = requests.post(
    'https://ymg.estes-express.com/prweb/app/YardMgmt/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
    params=params,
    data=data,
)


params = {
    'pyActivity': 'DoClose',
    'pzFromFrame': 'pyWorkPage',
    'pzPrimaryPageName': 'pyWorkPage',
    'pyRemCtlExpProp': 'true',
    'pzHarnessID': 'HIDC41386C835D250D4B683944019B72FD4',
    'AJAXTrackID': '2',
    'retainLock': 'false',
    'dcCleanup': 'true',
}

response = requests.get(
    'https://ymg.estes-express.com/prweb/app/YardMgmt/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator',
    params=params,
)


params = {
    'pzTransactionId': '2619a4d4e5f1e5a6edda54c98dc249f7',
}

data = 'isDCSPA=true&AJAXTrackID=20&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=HARNESS&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OGapIdentifier=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput=&$OpxVisible=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OForm=&$OHarness=&$OLGBundle=&$OLayoutGroup=&$OListView_FilterPanel_Btns=&$OListView_header=&$OMicroDynamicContainer=&$OPegaSocial=&$ORepeatingGrid=&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&$OpxGridHeaderRow=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxMicroDynamicContainer=&$OpxTextArea=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpxWorkAreaHeader=&$OpyDirtyCheckConfirm=&$Opycosmoscustomscripts=&$OpzLocalActionScript=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes=&$Opzcosmosuiscripts=&$Opzpega_control_attachcontent=&$OGridInc=&isURLReady=true&api=activate&UITemplatingStatus=Y&inStandardsMode=true&pzHarnessID=HID9484605AE427292FC7D02AB93F064856'

response = requests.post(
    'https://ymg.estes-express.com/prweb/app/YardMgmt/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!STANDARD',
    params=params,
    data=data,
)