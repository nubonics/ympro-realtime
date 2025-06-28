import logging


class TransferTask:
    """
    Transfers a Pega yard task to a new assignee.
    Usage:
        transfer = TransferTask(task_id, assigned_to)
        transfer.set_pega_data(...)
        await transfer.transfer_task()
    """

    def __init__(self, task_id: str, assigned_to: str):
        self.task_id = task_id
        self.assigned_to = assigned_to
        self.async_client = None
        self.details_url = None
        self.pzHarnessID = None
        self.csrf_token = None
        self.fingerprint_token = None
        self.logger = logging.getLogger(__name__)

    def set_pega_data(
            self,
            details_url: str,
            pzHarnessID: str,
            async_client,
            csrf_token: str = None,
            fingerprint_token: str = None,
    ):
        self.details_url = details_url
        self.pzHarnessID = pzHarnessID
        self.async_client = async_client
        self.csrf_token = csrf_token
        self.fingerprint_token = fingerprint_token

    async def transfer_task(self):
        """
        Transfers the given task to the new assignee.
        Returns the response object.
        """
        params = {
            'pzTransactionId': '',
            'pzFromFrame': 'pyWorkPage',
            'pzPrimaryPageName': 'pyWorkPage',
            'AJAXTrackID': '6',
            'eventSrcSection': 'Data-Portal.PortalNavigation',
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
            'Referer': self.details_url,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0',
            'X-Requested-With': 'XMLHttpRequest',
            'pzBFP': self.fingerprint_token or '',
            'pzCTkn': self.csrf_token or '',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        assignment_handle = (
            f'ASSIGN-INTERNAL ESTES-OPS-YARDMGMT-WORK {self.task_id}!PZINTERNALCASEFLOW'
        )
        data = (
            f'pyActivity=ProcessAction'
            f'&$PpyWorkPage$ppyInternalAssignmentHandle={assignment_handle}'
            f'&HarnessType=Review'
            f'&Purpose=Review'
            f'&$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType=WORK'
            f'&UITemplatingStatus=Y'
            f'&NewTaskStatus=TransferTask'  # This activity may differ; adjust if needed
            f'&TaskIndex='
            f'&StreamType=Rule-HTML-Section'
            f'&FieldError=&FormError=NONE&pyCustomError=pyCaseErrorSection'
            f'&bExcludeLegacyJS=true&ModalSection=pzModalTemplate'
            f'&modalStyle=&IgnoreSectionSubmit=true'
            f'&bInvokedFromControl=true&BaseReference=&isModalFlowAction=true'
            f'&bIsModal=true&bIsOverlay=false'
            f'&StreamClass=Rule-HTML-Section&UITemplatingScriptLoad=true'
            f'&ActionSection=pzModalTemplate'
            f'&pzHarnessID={self.pzHarnessID}'
            f'&inStandardsMode=true'
            f'&eventSrcSection=Data-Portal.PortalNavigation'
            f'&AssignedTo={self.assigned_to}'
        )

        self.logger.info(f"Transferring Pega YardMgmt task: {self.task_id} to {self.assigned_to}")
        resp = await self.async_client.post(
            self.details_url, params=params, headers=headers, data=data
        )
        if resp.status_code == 200:
            self.logger.info(f"Transfer task {self.task_id} request succeeded.")
        else:
            self.logger.warning(f"Transfer task {self.task_id} request failed: {resp.status_code} {resp.text[:200]}")
        return resp
