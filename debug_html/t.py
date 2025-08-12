import requests

cookies = {
    'Pega-Perf': 'itkn=13&start',
    'Pega-RULES': '%09%7Bpd%7DAAAAD7urY3Ez7sLzFoSNk3hcT%2FR6UqhR%2FB5obtWOlkOfF0K11b%2BDCMSr4uSq1PhF0jMUmA%3D%3DA%7Bapp%7D',
    'JSESSIONID': '31A8D918D6508DEFD52209ECD7915C16',
    'NSC_MC-ZBSE-QSE-TTM': 'ffffffff09173d9245525d5f4f58455e445a4a4229a0',
}

import httpx

# Replace these with your actual values from DevTools/HAR/cURL
url = "https://ymg.estes-express.com/prweb/app/YardMgmt/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!DCSPA_YardCoordinator?pzTransactionId=b680fd01df9bf0bbe85c1bf5939709ec&pzFromFrame=&pzPrimaryPageName=pyDisplayHarness&AJAXTrackID=25"

# Paste your cookies from browser here (if needed)
cookies = {
    "JSESSIONID": "<your_session_id>",
    "Pega-RULES": "<your_pega_rules>",
    "NSC_MC-ZBSE-QSE-TTM": "<your_nsc_cookie>",
    # Add any additional cookies that appear in your browser
}

cookie_header = (
    "Pega-Perf=itkn=13&start; "
    "Pega-RULES=%09%7Bpd%7DAAAAD7urY3Ez7sLzFoSNk3hcT%2FR6UqhR%2FB5obtWOlkOfF0K11b%2BDCMSr4uSq1PhF0jMUmA%3D%3DA%7Bapp%7D; "
    "JSESSIONID=31A8D918D6508DEFD52209ECD7915C16; "
    "NSC_MC-ZBSE-QSE-TTM=ffffffff09173d9245525d5f4f58455e445a4a4229a0"
)

headers = {
    "Accept": "*/*",
    "Cookie": cookie_header,
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "DNT": "1",
    "Host": "ymg.estes-express.com",
    "Origin": "https://ymg.estes-express.com",
    "Pragma": "no-cache",
    "Referer": "https://ymg.estes-express.com/prweb/app/YardMgmt/hHmgZBid4qBLDA0jxjIe6kTOQ39_jCSD*/!STANDARD?pzPostData=-1084884441",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "pzBFP": "{v2}7be0183013f68fa5d30a88742234aa78",
    "pzCTkn": "af8e5da56ab58a49e58e4b0a044a1521",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
}

# Paste your POST data here, exactly as seen in the HAR/cURL, as a string
# You can copy the raw text from DevTools > Network > Payload
data = """
pyActivity=pzRunActionWrapper&$OCompositeGadget=&$OControlMenu=&$ODesktopWrapperInclude=&$ODeterminePortalTop=&$ODynamicContainerFrameLess=&$ODynamicLayout=&$ODynamicLayoutCell=&$OEvalDOMScripts_Include=&$OGapIdentifier=&$OHarnessStaticJSEnd=&$OHarnessStaticJSStart=&$OHarnessStaticScriptsClientValidation=&$OHarnessStaticScriptsExprCal=&$OLaunchFlow=&$OMenuBar=&$OMenuBarOld=&$OMobileAppNotify=&$OOperatorPresenceStatusScripts=&$OPMCPortalStaticScripts=&$ORepeatingDynamicLayout=&$OSessionUser=&$OSurveyStaticScripts=&$OWorkformStyles=&$Ocosmoslocale=&$OmenubarInclude=&$OpxButton=&$OpxDisplayText=&$OpxDropdown=&$OpxDynamicContainer=&$OpxHidden=&$OpxIcon=&$OpxLayoutContainer=&$OpxLayoutHeader=&$OpxLink=&$OpxMenu=&$OpxNonTemplate=&$OpxSection=&$OpxTextInput=&$OpxVisible=&$OpyWorkFormStandardEnd=&$OpyWorkFormStandardStart=&$Opycosmoscustomstyles=&$OpzAppLauncher=&$OpzDecimalInclude=&$OpzFrameLessDCScripts=&$OpzHarnessInlineScriptsEnd=&$OpzHarnessInlineScriptsStart=&$OpzPegaCompositeGadgetScripts=&$OpzRuntimeToolsBar=&$Opzpega_ui_harnesscontext=&$Ordlincludes=&$OxmlDocumentInclude=&$OForm=&$OGridInc=&$OHarness=&$OpxHarnessContent=&$OpxHeaderCell=&$OpxWorkArea=&$OpxWorkAreaContent=&$OpyDirtyCheckConfirm=&$OCheckbox=&ThreadName=&rowPage=D_TeamMembersByWorkGroup_pa1447668436513772pz.pxResults(8)&Location=pyActivity%3DpzPrepareAssignment%26UITemplatingStatus%3DY%26NewTaskStatus%3DDisplayUserWorkList%26TaskIndex%3D%26StreamType%3DRule-HTML-Section%26FieldError%3D%26FormError%3D%26pyCustomError%3D%26bExcludeLegacyJS%3Dtrue%26ModalSection%3DpzModalTemplate%26modalStyle%3D%26IgnoreSectionSubmit%3Dtrue%26bInvokedFromControl%3Dtrue%26BaseReference%3D%26isModalFlowAction%3Dtrue%26bIsModal%3Dtrue%26bIsOverlay%3Dfalse%26StreamClass%3DRule-HTML-Section%26UITemplatingScriptLoad%3Dtrue%26ActionSection%3DpzModalTemplate%26rowPage%3DD_TeamMembersByWorkGroup_pa1447668436513772pz.pxResults(8)%26GridAction%3Dtrue%26BaseThread%3DDCSPA_YardCoordinator%26pzHarnessID%3DHID851B7BD23A0C9961EF2CF02DA01D9FCB&PagesToCopy=D_TeamMembersByWorkGroup_pa1447668436513772pz&pzHarnessID=HID6A2A89D4090E6F8EB6540FCAA07843DB&UITemplatingStatus=N&inStandardsMode=true&pzActivity=pzPerformGridAction&skipReturnResponse=true&pySubAction=runAct
""".strip()

async def main():
    async with httpx.AsyncClient(cookies=cookies) as client:
        response = await client.post(url, headers=headers, data=data, follow_redirects=False)
        print(f"Status: {response.status_code}")
        print(f"Headers: {response.headers}")
        print("Body (truncated):")
        print(response.text[:800])  # truncate for preview
        # Save the full HTML if needed
        with open("hostler_select_task.html", "w", encoding="utf-8") as f:
            f.write(response.text)

import asyncio; asyncio.run(main())