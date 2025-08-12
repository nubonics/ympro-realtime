from uuid import uuid4
import requests
import re

# Step 1: GET the homepage (STANDARD)
headers_homepage = {
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=0, i',
    'cookie': 'Pega-RULES=%09%7Bpd%7DAAAADyA43%2Bk7%2BEtLXwd8qdEld%2FosFxEO44%2B0pPeZb%2BdITS%2FvSA0dfwi8ey%2BxQr4NG18uiA%3D%3DA%7Bapp%7D; JSESSIONID=1BCB9160E4A11CEF3414CD58A04096AB; NSC_MC-ZBSE-QSE-TTM=ffffffff09173d9345525d5f4f58455e445a4a4229a0'
}
url_homepage = "https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!STANDARD?pzPostData=1263097320"

response0 = requests.get(url_homepage, headers=headers_homepage)
with open("homepage.html", "wb") as f:
    f.write(response0.content)

# Step 2: Extract dynamicContainerID (tabGrpName) from homepage
dynamic_container_id = None
match = re.search(r'"tabGrpName"\s*:\s*"([0-9a-fA-F\-]{36})"', response0.text)
if match:
    dynamic_container_id = match.group(1)
else:
    match2 = re.search(r'tabGrpName\s*=\s*[\'"]([0-9a-fA-F\-]{36})[\'"]', response0.text)
    if match2:
        dynamic_container_id = match2.group(1)

print("Extracted dynamicContainerID:", dynamic_container_id)

# Step 3: POST to the reports portal navigation using extracted dynamicContainerID
headers_reports = {
    'content-length': '1717',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'pzbfp': '{v2}2b8a586272dbb157246f9b3a1e5abc9d',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded',
    'pzctkn': '86ba315d1786cf3ba08636aa9cc6dd70',
    'accept': '*/*',
    'origin': 'https://ymg.estes-express.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'cookie': 'Pega-Perf=itkn=1&start; Pega-RULES=%09%7Bpd%7DAAAADyA43%2Bk7%2BEtLXwd8qdEld%2FosFxEO44%2B0pPeZb%2BdITS%2FvSA0dfwi8ey%2BxQr4NG18uiA%3D%3DA%7Bapp%7D; JSESSIONID=1BCB9160E4A11CEF3414CD58A04096AB; NSC_MC-ZBSE-QSE-TTM=ffffffff09173d9345525d5f4f58455e445a4a4229a0'
}

payload_template = (
    'pyActivity=%40baseclass.doUIAction&isDCSPA=true&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop='
    '&$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OForm='
    '&$OGapIdentifier=&$OGridInc=&$OHarness=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart='
    '&$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar='
    '&$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts='
    '&$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale='
    '&$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer='
    '&$OpxHarnessContent=&$OpxHeaderCell=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer='
    '&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput='
    '&$OpxVisible=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpyDirtyCheckConfirm='
    '&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles='
    '&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd='
    '&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar='
    '&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude='
    '&isSDM=true&action=display&label=Reports&className=ESTES-OPS-YardMgmt-UIPages'
    '&harnessName=Reports&contentID={contentID}&dynamicContainerID={dynamicContainerID}&SkipConflictCheck=true'
    '&readOnly=false&tabName=Reports&replaceCurrent=false&api=display'
    '&portalName=YardCoordinator&portalThreadName=STANDARD&tabIndex=1'
    '&pzHarnessID=HID588BF0008128A1124103C6D4E9E8E6F1&UITemplatingStatus=Y&inStandardsMode=true&eventSrcSection=Data-Portal.PortalNavigation'
)

contentID = str(uuid4())
if dynamic_container_id:
    payload = payload_template.format(contentID=contentID, dynamicContainerID=dynamic_container_id)
else:
    print("WARNING: dynamicContainerID not found, using random")
    payload = payload_template.format(contentID=contentID, dynamicContainerID=str(uuid4()))

url_reports = "https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator?eventSrcSection=Data-Portal.PortalNavigation"
response1 = requests.post(url_reports, headers=headers_reports, data=payload.encode('utf-8'))
with open("reports_portal.html", "wb") as f:
    f.write(response1.content)

print("Step 2 POST status:", response1.status_code)

# Step 4: GET the actual reports page (shortcut)
headers_shortcut = {
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': url_homepage,
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=0, i',
    'cookie': 'Pega-Perf=itkn=1; Pega-RULES=%09%7Bpd%7DAAAADyA43%2Bk7%2BEtLXwd8qdEld%2FosFxEO44%2B0pPeZb%2BdITS%2FvSA0dfwi8ey%2BxQr4NG18uiA%3D%3DA%7Bapp%7D; JSESSIONID=54CF4D144A0413BC5AD4BC062492BC82; NSC_MC-ZBSE-QSE-TTM=ffffffff09173d9345525d5f4f58455e445a4a4229a0'
}
url_shortcut = (
    "https://ymg.estes-express.com/prweb/app/YardMgmt_/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator"
    "?pyActivity=%40baseclass.doUIAction"
    "&pyReportClass=ESTES-OPS-YardMgmt-Work-Task"
    "&pyShortcutHandle=YARDMANAGEMENT!S!ALL!TASKLISTBYJOCKEYWISE"
    "&action=reportDefinition"
    "&ReportAction=shortcut"
    "&pyDisplayTarget=popup"
    "&target=popup"
    "&portalThreadName=DCSPA_YardCoordinator"
    "&portalName=YardCoordinator"
    "&eventSrcSection=Data-Portal.PortalNavigation"
    "&pzHarnessID=HID588BF0008128A1124103C6D4E9E8E6F1"
)

response2 = requests.get(url_shortcut, headers=headers_shortcut)
with open("reports_page.html", "wb") as f:
    f.write(response2.content)

print("Step 3 GET shortcut status:", response2.status_code)