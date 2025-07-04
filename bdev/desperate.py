import requests

cookies = {
    'Pega-Perf': 'itkn=23&start',
    'Pega-RULES': '%09%7Bpd%7DAAAAD7Cql28bOBY%2FVtcy3I6M00sKWyvtAMDW%2FD8divS5H5nSv6z8frb2Qei1OhUdqEUwRA%3D%3DA%7Bapp%7D',
    'JSESSIONID': 'FB4BD517AB8E5F05BC2A27ECFE594887',
    'NSC_MC-ZBSE-QSE-TTM': 'ffffffff09173d9545525d5f4f58455e445a4a4229a0',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'DNT': '1',
    'Origin': 'https://ymg.estes-express.com',
    'Pragma': 'no-cache',
    # 'Referer': 'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!STANDARD?pzPostData=1466265057',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'pzBFP': '{v2}7be0183013f68fa5d30a88742234aa78',
    'pzCTkn': '0773ba392eb98180d259915c898aee48',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'Pega-Perf=itkn=23&start; Pega-RULES=%09%7Bpd%7DAAAAD7Cql28bOBY%2FVtcy3I6M00sKWyvtAMDW%2FD8divS5H5nSv6z8frb2Qei1OhUdqEUwRA%3D%3DA%7Bapp%7D; JSESSIONID=FB4BD517AB8E5F05BC2A27ECFE594887; NSC_MC-ZBSE-QSE-TTM=ffffffff09173d9545525d5f4f58455e445a4a4229a0',
}

params = {
    'pzTransactionId': '',
    'pzFromFrame': '',
    'pzPrimaryPageName': 'pyPortalHarness',
    'AJAXTrackID': '2',
}

data = 'pzuiactionzzz=CXt0cn17U1RBTkRBUkR9NGZlNTE2MTljNTkzOTQ4ZjIyODkyZTY0ZTk0ZWFjNmEwM2UyYjZjMTY1MzlmYTZjMWMzOWM5YTAyYzJhZDkzNGU5ZjY4NThkMTAxOWQyMDI5NGIyODY4ZTNhNDQ4YTc1ODYyODNkNmY3OWY1NzYzNjg5ZjYwODEzODAwZDM0NmM5OTFjOWE1MmIzNzYwMzBmNmYwNTI5NmFhM2U1OTYwMDFlYmExNDMwM2I5NzdkOTE2ZDZlZTFhZjE2MDg0ZDhjYzJkYzg2ZGUyZDg1ZTBhOTYxMDQ3MmUyZDQ5NTIwNmNlYWIwZWQ3YmY0N2U4MWNiN2M3N2RiMGYyZThjMTE5YjI0N2MxNjdlMDlhNTEyMGU0MGNlMzgwMGZmYmZjNjhlNmFiZDRjOTc1YjRhNGMwZGEyMWVmYjZhYjljOWFkYTdlMWQyMDEzMTM2NWU5NGViMzIxMjIyYjYzYTYwZTJlYzdjOGM0MWUwYzI5M2VlOTA4NDk2Y2FjNGQ2N2RlODQ1ZDk2M2U3MjQwNjRmYTc2MGI0MmQxNTRjY2NiMmU0ZTZiNDE3YmEzZGFlZmQ4ZmNiNDRiNmI0Yzk5NzQ1NTYxOTU5N2VmMTMzYWM5NTgzOTZjZjIwMzc2MjAzMDI5YTYyZDNkNjI2MWYwNjdhOGVlNjYxYzEwNGZhZDY4ZjY3ZmEyYTQzOTUyNzhlNWFjZWUxOWVjNzgyZDA5YWEzZGI2Y2MxZGNlOGQwMDA2MjQ2Njc5NDQyNjM3NDQxY2JiY2Nm*=&pySearchString=T-34388517&pzActivityParams=pySearchString&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=HARNESS&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OGapIdentifier=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput=&$OpxVisible=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OForm=&$OHarness=&$OLGBundle=&$OLayoutGroup=&$OListView_FilterPanel_Btns=&$OListView_header=&$OMicroDynamicContainer=&$OPegaSocial=&$ORepeatingGrid=&$OpxGrid=&$OpxGridBody=&$OpxGridDataCell=&$OpxGridDataRow=&$OpxGridHeaderCell=&$OpxGridHeaderRow=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxMicroDynamicContainer=&$OpxTextArea=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpxWorkAreaHeader=&$OpyDirtyCheckConfirm=&$Opycosmoscustomscripts=&$OpzLocalActionScript=&$OpzMicroDynamicContainerScripts=&$OpzTextIncludes=&$Opzcosmosuiscripts=&$Opzpega_control_attachcontent=&$OGridInc=&$OCheckbox=&UITemplatingStatus=N&inStandardsMode=true&pzHarnessID=HID653B94938D429F6907B2CAE855FBD914'

response = requests.post(
    'https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!STANDARD',
    params=params,
    # cookies=cookies,
    headers=headers,
    data=data,
)
print(f'[Step 1] session cookies: {response.cookies.get_dict()}')

print(response.status_code)
with open('response.html', 'w') as writer:
    writer.write(response.text)

if 'true' in response.text.lower():
    print(True)
