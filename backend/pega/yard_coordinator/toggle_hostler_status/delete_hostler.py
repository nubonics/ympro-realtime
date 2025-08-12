import logging
import re
import urllib.parse
import uuid

logger = logging.getLogger(__name__)


class DeleteHostler:
    """
    Handles the deletion of a hostler to force status offline.
    Mirrors the sequence of Pega UI steps as captured in your cURLs (steps 1-7).
    """

    def __init__(self, session_manager, hostler):
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

    @staticmethod
    def extract_step4_pzuiactionzzz(html: str):
        candidates = []
        for m in re.findall(r'pzuiactionzzz[=\\u003d]+([A-Za-z0-9%*]+)', html):
            decoded = urllib.parse.unquote(m)
            candidates.append(decoded)
        for m in re.findall(r'"pzuiactionzzz[=\\u003d]+([A-Za-z0-9%*]+)"', html):
            decoded = urllib.parse.unquote(m)
            candidates.append(decoded)
        if candidates:
            return max(candidates, key=len)
        return None

    @staticmethod
    def extract_step7_pzuiactionzzz(html: str):
        matches = re.findall(r'pzuiactionzzz[=\\u003d]+([A-Za-z0-9%*]+)', html)
        if matches:
            return matches[0]
        return None

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

    async def run(self):
        # Step 1: Open Operators harness
        await self.post(self.step1_data())
        # Step 2: Filter/search for operator in grid
        await self.post(self.step2_data())
        # Step 3: Search for operator by user_identifier (get pzuiactionzzz from HTML if needed)
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
        step7_pzuiactionzzz = self.extract_step7_pzuiactionzzz(resp7.text)
        return step7_pzuiactionzzz  # Pass this to the create step
