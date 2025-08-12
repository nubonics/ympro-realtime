import logging
import uuid


logger = logging.getLogger(__name__)


class CreateHostler:
    """
    Handles the creation (re-insertion) of a hostler.
    Steps 8-12.
    """

    def __init__(self, session_manager, hostler):
        self.session_manager = session_manager
        self.async_client = session_manager.async_client
        self.base_url = session_manager.base_url
        self.pzHarnessID = session_manager.pzHarnessID
        self.details_url = session_manager.details_url
        self.content_id = str(uuid.uuid4())
        self.hostler = hostler

    def get_headers(self):
        headers = self.session_manager.get_standard_headers()
        headers["Referer"] = f"{self.base_url}"
        return headers

    def step8_data(self, pzuiactionzzz):
        # Search for the operator again (after delete)
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

    def step9_data(self, pzuiactionzzz):
        # Confirm grid after delete
        return self.step8_data(pzuiactionzzz)

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
            f"&$PInsertOpPage$pYardMgmtAccessGroup=YardMgmt:Users"
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

    async def run(self, initial_pzuiactionzzz):
        # Step 8: Search again by identifier
        resp8 = await self.post(self.step8_data(initial_pzuiactionzzz))
        # Step 9: Confirm grid after delete (could extract new pzuiactionzzz if needed)
        await self.post(self.step9_data(initial_pzuiactionzzz))
        # Step 10: ProcessAction - InsertOperator
        await self.post(self.step10_data())
        # Step 11: SubmitModalFlowAction (create operator)
        res = await self.post(self.step11_data())
        # Step 12: Final grid refresh (if needed, supply real pzTransactionId)
        step_12_pzTransactionId = res.text.split('||')[1]
        await self.post(self.step12_data(step_12_pzTransactionId))
