import logging
from typing import Optional


class DeleteTask:
    """
    Encapsulates the logic to delete a task in Pega YardMgmt via the async_client session.
    Usage:
        deleter = DeleteTask(task_id)
        # Set session and Pega vars:
        deleter.set_pega_data(...)
        result = await deleter.delete_task()
    """

    def __init__(self, task_id: str):
        self.task_id = task_id
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
            csrf_token: Optional[str] = None,
            fingerprint_token: Optional[str] = None,
    ):
        self.details_url = details_url
        self.pzHarnessID = pzHarnessID
        self.async_client = async_client
        self.csrf_token = csrf_token
        self.fingerprint_token = fingerprint_token

    async def delete_task(self):
        """
        Deletes a task by its T-XXXX id using the current pega async session.
        Returns the response object.
        """
        # The form data is based on reverse engineering the Pega YardMgmt UI network calls.
        params = {
            'pzTransactionId': '',
            'pzFromFrame': 'pyWorkPage',
            'pzPrimaryPageName': 'pyWorkPage',
            'AJAXTrackID': '5',
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
            f'&NewTaskStatus=DeleteTask'
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
        )

        self.logger.info(f"Deleting Pega YardMgmt task: {self.task_id}")
        resp = await self.async_client.post(
            self.details_url, params=params, headers=headers, data=data
        )
        if resp.status_code == 200:
            self.logger.info(f"Delete task {self.task_id} request succeeded.")
        else:
            self.logger.warning(f"Delete task {self.task_id} request failed: {resp.status_code} {resp.text[:200]}")
        return resp
