import urllib.parse

data = 'isDCSPA=true&AJAXTrackID=2&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=HARNESS&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OGapIdentifier=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput=&$OpxVisible=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OForm=&$OGridInc=&$OHarness=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpyDirtyCheckConfirm=&$OCheckbox=&$OLGBundle=&$OLayoutGroup=&$OListView_FilterPanel_Btns=&$OListView_header=&$OMicroDynamicContainer=&$OPegaSocial=&$ORepeatingGrid=&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&$OpxGridHeaderRow=&$OpxMicroDynamicContainer=&$OpxTextArea=&$OpxWorkAreaHeader=&$Opycosmoscustomscripts=&$OpzLocalActionScript=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes=&$Opzcosmosuiscripts=&$Opzpega_control_attachcontent=&$OpxRadioButtons=&$OlfsInclude=&$OpxCheckbox=&$OpxAutoComplete=&$OpzAutoCompleteAGIncludes=&$OListViewIncludes=&$OpzRadiogroupIncludes=&isURLReady=true&api=activate&UITemplatingStatus=Y&inStandardsMode=true&pzHarnessID=HIDAFE941E341451946936AC79C109819DF'


def query_to_dict(query):
    result = {}
    pairs = query.split("&")
    for pair in pairs:
        if "=" in pair:
            key, value = pair.split("=", 1)
            result[urllib.parse.unquote(key)] = urllib.parse.unquote(value)
        else:
            result[pair] = ""
    return result

data_dict = query_to_dict(data)
print(data_dict)