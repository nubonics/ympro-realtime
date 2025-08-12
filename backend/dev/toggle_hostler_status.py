import logging
import re
import urllib.parse
import uuid
from typing import Sized

from backend.pega.yard_coordinator.session_manager.models import ReCreateHostler

logger = logging.getLogger(__name__)


class ToggleHostlerStatus:
    """
    Delete and re-create a hostler to force status offline.
    Mirrors the sequence of Pega UI steps as captured in your cURLs.
    """

    def __init__(self, session_manager, hostler: "ReCreateHostler"):
        self.session_manager = session_manager
        self.async_client = session_manager.async_client
        self.base_url = session_manager.base_url
        self.pzHarnessID = session_manager.pzHarnessID
        self.fingerprint_token = session_manager.fingerprint_token
        self.csrf_token = session_manager.csrf_token
        self.details_url = session_manager.details_url
        self.content_id = str(uuid.uuid4())
        self.hostler = hostler
        self.pzuiactionzzz = session_manager.pzuiactionzzz

    def get_headers(self):
        headers = self.session_manager.get_standard_headers()
        headers["Referer"] = f"{self.base_url}"
        return headers

    # Each step below returns the POST data for that step
    def step1_data(self):
        # Open Operators harness
        return (
            "pyActivity=%40baseclass.doUIAction&isDCSPA=true"
            "&action=display&label=Operators"
            "&className=ESTES-OPS-YardMgmt-UIPages"
            "&harnessName=Operators"
            f"&contentID={self.content_id}"
            "&SkipConflictCheck=true"
            "&readOnly=false"
            "&tabName=Operators&replaceCurrent=false"
            "&api=display"
            "&portalName=YardCoordinator&portalThreadName=STANDARD&tabIndex=1"
            f"&pzHarnessID={self.pzHarnessID}"
            "&UITemplatingStatus=Y&inStandardsMode=true&eventSrcSection=Data-Portal.PortalNavigation"
        )

    def step2_data(self):
        # Filter/search for operator by user_identifier
        return (
            "pyActivity=ReloadSection"
            "&AC_Grid_FilterParamValue=j"
            "&UITemplatingStatus=N"
            "&StreamClass=Rule-HTML-Section"
            "&bClientValidation=true"
            "&ReadOnly=0"
            "&StreamName=ManageOperators"
            "&RenderSingle=InitialRender_EXPANDEDSubSectionManageOperators8_pySearchText"
            "&AC_PropPage=pyDisplayHarness"
            "&BaseReference="
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
            "&eventSrcSection=Data-Portal.PortalNavigation"
        )

    def step3_data(self, pzuiactionzzz):
        # Search for operator by user_identifier
        return (
            f"$PpyDisplayHarness$ppySearchText={self.hostler.checker_id}"
            "&OperatorListPpxResults1colWidthGBL=&OperatorListPpxResults1colWidthGBR="
            f"&pzuiactionzzz={pzuiactionzzz}"
            "&PreActivitiesList=&sectionParam="
            f"&ActivityParams=UserIdentifier%3D{self.hostler.checker_id}"
            "&pyEncodedParameters=true"
            "&pzKeepPageMessages=false"
            "&strPHarnessClass=ESTES-OPS-YardMgmt-UIPages"
            "&strPHarnessPurpose=Operators"
            "&UITemplatingStatus=Y"
            "&StreamName=ManageOperators"
            "&BaseReference="
            "&bClientValidation=true"
            "&HeaderButtonSectionName=-1"
            "&PagesToRemove="
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
            "&eventSrcSection=Data-Portal.PortalNavigation"
        )

    def step4_data(self, pzuiactionzzz):
        # Confirm delete modal
        return (
            f"$PpyDisplayHarness$ppySearchText={self.hostler.checker_id}"
            "&OperatorListPpxResults1colWidthGBL=&OperatorListPpxResults1colWidthGBR="
            f"&pzuiactionzzz={pzuiactionzzz}"
            "&PreActivitiesList=&sectionParam="
            "&ActivityParams=%3D"
            "&pyEncodedParameters=true"
            "&pzKeepPageMessages=false"
            "&strPHarnessClass=ESTES-OPS-YardMgmt-UIPages"
            "&strPHarnessPurpose=Operators"
            "&UITemplatingStatus=Y"
            "&StreamName=ManageOperators"
            "&BaseReference="
            "&bClientValidation=true"
            "&HeaderButtonSectionName=-1"
            "&PagesToRemove="
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
            "&eventSrcSection=Data-Portal.PortalNavigation"
        )

    def step5_data(self):
        # ProcessAction - ConfirmDeleteOperator
        return (
            "pyActivity=ProcessAction"
            "&UITemplatingStatus=Y"
            "&NewTaskStatus=ConfirmDeleteOperator"
            "&TaskIndex="
            "&StreamType=Rule-HTML-Section"
            "&FieldError=&FormError=&pyCustomError="
            "&bExcludeLegacyJS=true"
            "&ModalSection=pzModalTemplate&modalStyle="
            "&BaseReference=DeleteOpPage"
            "&IgnoreSectionSubmit=true"
            "&bInvokedFromControl=true"
            "&isModalFlowAction=true"
            "&bIsModal=true"
            "&bIsOverlay=false"
            "&StreamClass=Rule-HTML-Section"
            "&UITemplatingScriptLoad=true"
            "&ActionSection=pzModalTemplate"
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
            "&eventSrcSection=Data-Portal.PortalNavigation"
        )

    def step6_data(self):
        # SubmitModalFlowAction (delete)
        return (
            "pyActivity=SubmitModalFlowAction"
            "&actionName=ConfirmDeleteOperator"
            "&KeepMessages=false"
            "&modalSection=pzModalTemplate"
            "&bIsOverlay=false"
            "&InterestPage=DeleteOpPage"
            "&HarnessType=NEW"
            "&UITemplatingStatus=Y"
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
            "&eventSrcSection=Data-Portal.PortalNavigation"
        )

    def step7_data(self, pzuiactionzzz):
        # Refresh grid after delete
        return (
            f"$PpyDisplayHarness$ppySearchText={self.hostler.checker_id}"
            "&OperatorListPpxResults1colWidthGBL=&OperatorListPpxResults1colWidthGBR="
            f"&pzuiactionzzz={pzuiactionzzz}"
            "&PreActivitiesList=&sectionParam="
            "&ActivityParams=%3D"
            "&pyEncodedParameters=true"
            "&pzKeepPageMessages=false"
            "&strPHarnessClass=ESTES-OPS-YardMgmt-UIPages"
            "&strPHarnessPurpose=Operators"
            "&UITemplatingStatus=Y"
            "&StreamName=ManageOperators"
            "&BaseReference="
            "&bClientValidation=true"
            "&HeaderButtonSectionName=-1"
            "&PagesToRemove="
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
        )

    def step8_data(self, pzuiactionzzz):
        # Search for the operator again (after delete)
        return self.step3_data(pzuiactionzzz)

    def step9_data(self, pzuiactionzzz):
        # Confirm grid after delete
        return self.step7_data(pzuiactionzzz)

    def step10_data(self):
        # ProcessAction - InsertOperator (re-create)
        return (
            "pyActivity=ProcessAction"
            "&UITemplatingStatus=Y"
            "&NewTaskStatus=InsertOperator"
            "&TaskIndex="
            "&StreamType=Rule-HTML-Section"
            "&FieldError=&FormError=&pyCustomError="
            "&bExcludeLegacyJS=true"
            "&ModalSection=pzModalTemplate&modalStyle="
            "&BaseReference=InsertOpPage"
            "&IgnoreSectionSubmit=true"
            "&bInvokedFromControl=true"
            "&isModalFlowAction=true"
            "&bIsModal=true"
            "&bIsOverlay=false"
            "&StreamClass=Rule-HTML-Section"
            "&UITemplatingScriptLoad=true"
            "&ActionSection=pzModalTemplate"
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
        )

    def step11_data(self):
        # SubmitModalFlowAction (create operator)
        return (
            "pyActivity=SubmitModalFlowAction"
            f"&$PInsertOpPage$ppyUserIdentifier={self.hostler.checker_id}"
            f"&$PInsertOpPage$pUserName=%20{self.hostler.hostler_name}"
            f"&$PInsertOpPage$pPassword={self.hostler.password}"
            f"&$PInsertOpPage$pYardMgmtAccessGroup={self.hostler.access_group}"
            "&actionName=InsertOperator"
            "&KeepMessages=false"
            "&modalSection=pzModalTemplate"
            "&bIsOverlay=false"
            "&InterestPage=InsertOpPage"
            "&HarnessType=NEW"
            "&UITemplatingStatus=Y"
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
            "&eventSrcSection=Data-Portal.PortalNavigation"
        )

    def step12_data(self, pzTransactionId):
        # Final grid refresh after re-create
        return (
            f"$PpyDisplayHarness$ppySearchText={self.hostler.checker_id}"
            "&OperatorListPpxResults1colWidthGBL=&OperatorListPpxResults1colWidthGBR="
            # pzuiactionzzz might need to be updated here
            "&PreActivitiesList=&sectionParam="
            "&ActivityParams=%3D"
            "&pyEncodedParameters=true"
            "&pzKeepPageMessages=false"
            "&strPHarnessClass=ESTES-OPS-YardMgmt-UIPages"
            "&strPHarnessPurpose=Operators"
            "&UITemplatingStatus=Y"
            "&StreamName=ManageOperators"
            "&BaseReference="
            "&bClientValidation=true"
            "&HeaderButtonSectionName=-1"
            "&PagesToRemove="
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
            f"&pzTransactionId={pzTransactionId}"
        )

    async def post(self, data):
        url = f"{self.base_url.replace('STANDARD', 'DCSPA_YardCoordinator')}"
        headers = self.get_headers()
        response = await self.async_client.post(
            url,
            headers=headers,
            data=data,
            follow_redirects=True
        )
        logger.debug(f"POST to {url} status {response.status_code}")
        return response

    @staticmethod
    def extract_step4_pzuiactionzzz(html: str) -> Sized | None:
        """
        Extracts the pzuiactionzzz value from a PEGA HTML page.
        Handles url-encoded, unicode-escaped, and JS-embedded forms.
        """
        # 1. Find all possible matches, including urlencoded and \u003d
        candidates = []

        # Match plain and unicode-escaped assignment
        for m in re.findall(r'pzuiactionzzz[=\\u003d]+([A-Za-z0-9%*]+)', html):
            # decode url-encoded just in case
            decoded = urllib.parse.unquote(m)
            candidates.append(decoded)

        # If also inside JSON, e.g. pzuiactionzzz=...%3D%3D*
        for m in re.findall(r'"pzuiactionzzz[=\\u003d]+([A-Za-z0-9%*]+)"', html):
            decoded = urllib.parse.unquote(m)
            candidates.append(decoded)

        # Return the longest candidate (sometimes first is truncated)
        if candidates:
            return max(candidates, key=len)
        return None

    @staticmethod
    def extract_step8_pzuiactionzzz(html: str) -> str | None:
        """
        Extracts the first pzuiactionzzz value as it appears in the HTML (no decoding).
        If there are multiple, returns the first.
        """
        matches = re.findall(r'pzuiactionzzz[=\\u003d]+([A-Za-z0-9%*]+)', html)
        if matches:
            return matches[0]  # or use matches[n] for nth, or all for a list
        return None

    @staticmethod
    def extract_step9_pzuiactionzzz(html: str) -> str | None:
        import re
        import urllib.parse
        candidates = []
        for m in re.findall(r'pzuiactionzzz[=\\u003d]+([A-Za-z0-9%*]+)', html):
            decoded = urllib.parse.unquote(m)
            candidates.append(decoded)
        if candidates:
            return max(candidates, key=len)
        return None

    async def run(self):
        # Step 3 and step 7 have the same pzuiactionzzz

        # Step 1: Open Operators harness
        await self.post(self.step1_data())
        # Step 2: Filter/search for operator in grid
        await self.post(self.step2_data())
        # Step 3: Search for operator by user_identifier (get pzuiactionzzz from HTML if needed)
        # TODO: Not sure if this is the correct pzuiactionzzz for step 3 only, the others steps are correct
        resp3 = await self.post(self.step3_data(self.session_manager.pzuiactionzzz))
        step4_pzuiactionzzz = self.extract_step4_pzuiactionzzz(resp3.text)
        # Step 4: Confirm delete modal (get pzuiactionzzz from HTML if needed)
        await self.post(self.step4_data(step4_pzuiactionzzz))
        # Step 5: Process delete modal
        await self.post(self.step5_data())
        # Step 6: Submit delete modal
        await self.post(self.step6_data())
        # Step 7: Refresh grid after delete
        resp7 = await self.post(self.step7_data(step4_pzuiactionzzz))
        step8_pzuiactionzzz = self.extract_step8_pzuiactionzzz(resp7.text)
        # Step 8: Search again by identifier
        resp8 = await self.post(self.step8_data(step8_pzuiactionzzz))
        step9_pzuiactionzzz = self.extract_step9_pzuiactionzzz(resp8.text)
        # Step 9: Confirm grid after delete
        await self.post(self.step9_data(step9_pzuiactionzzz))
        # Step 10: ProcessAction - InsertOperator
        await self.post(self.step10_data())
        # Step 11: SubmitModalFlowAction (create operator)
        res = await self.post(self.step11_data())
        # Step 12: Final grid refresh (if needed, supply real pzTransactionId)
        step_12_pzTransactionId = res.text.split('||')[1]
        await self.post(self.step12_data(step_12_pzTransactionId))

        logger.info("ToggleHostlerStatus flow completed.")
