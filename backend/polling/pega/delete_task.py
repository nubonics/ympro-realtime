import re
import urllib
import time
from lxml import html

from backend.colored_logger import setup_logger

logger = setup_logger(__name__)


class DeleteTask:
    """
    Deletes a Pega task by following the necessary open/process/close steps.
    Only requires task_id (e.g., "T-34246607") at construction.
    All session/context must be injected via set_pega_data().
    """

    def __init__(self, task_id):
        self.task_id = task_id  # e.g. "T-34246607"
        self.async_client = None
        self.base_url = None
        self.pzHarnessID = None
        self.csrf_token = None
        self.fingerprint_token = None
        self.details_url = None

        self.pega_url = None  # Will be set in set_pega_data

        self.pzTransactionId = None
        self.assignment_handle = None

    def set_pega_data(self, base_url, pzHarnessID, async_client, csrf_token, fingerprint_token, details_url=None):
        """
        Injects all session/context values required for deletion.
        """
        self.base_url = base_url.rstrip('/')
        self.pzHarnessID = pzHarnessID
        self.async_client = async_client
        self.csrf_token = csrf_token
        self.fingerprint_token = fingerprint_token
        self.details_url = details_url  # Not always needed for delete, but may be useful

        self.pega_url = self.base_url.replace('STANDARD', 'DCSPA_YardCoordinator')

    @staticmethod
    def _parse_html(html_content):
        try:
            tree = html.fromstring(html_content)
            return tree
        except Exception as e:
            logger.error("Failed to parse HTML: %s", e)
            return None

    def extract_pzTransactionId(self, html_content):
        tree = self._parse_html(html_content)
        if tree is None:
            return None
        xpath_expr = "//script[contains(text(), 'pega.ui.jittemplate.addMetadataTree')]"
        script_elements = tree.xpath(xpath_expr)
        if not script_elements:
            logger.warning("No script elements found for transaction id extraction")
            return None
        script_text = script_elements[0].text
        match = re.search(r"pzTransactionId=([^&\"\s]+)", script_text or "")
        return match.group(1) if match else None

    def extract_assignment_handle(self, html_content):
        """
        Extracts assignment handle (ASSIGN-INTERNAL ...) from the HTML content.
        """
        html_text = html_content.decode() if isinstance(html_content, bytes) else html_content
        match = re.search(r'ASSIGN-INTERNAL\s+ESTES-OPS-YARDMGMT-WORK\s+T-\d+!PZINTERNALCASEFLOW', html_text)
        if match:
            logger.debug(f"Extracted assignment handle: {match.group(0)}")
            return match.group(0)
        logger.warning("Assignment handle not found in HTML content.")
        return None

    async def open_task(self):
        """
        Opens the task in Pega and extracts required tokens for deletion.
        """
        params = {
            "eventSrcSection": "@baseclass.pyGroupBasketWork"
        }
        data = (
            "pyActivity=%40baseclass.doUIAction"
            "&isDCSPA=true"
            "&action=openWorkByHandle"
            f"&key=ESTES-OPS-YARDMGMT-WORK%20{self.task_id}"
            "&SkipConflictCheck=false"
            "&reload=false"
            "&api=openWorkByHandle"
            f"&contentID={int(time.time() * 1000)}"
            f"&dynamicContainerID={int(time.time() * 1000)}"
            "&portalName=YardCoordinator"
            "&portalThreadName=STANDARD"
            "&tabIndex=1"
            f"&pzHarnessID={self.pzHarnessID}"
            "&UITemplatingStatus=Y"
            "&inStandardsMode=true"
            "&eventSrcSection=%40baseclass.pyGroupBasketWork"
        )
        response = await self.async_client.post(
            url=self.pega_url,
            data=data,
            params=params,
            follow_redirects=True
        )
        logger.debug(f'DeleteTask: open_task status {response.status_code}')
        self.pzTransactionId = self.extract_pzTransactionId(response.content)
        self.assignment_handle = self.extract_assignment_handle(response.content)
        logger.debug(f'DeleteTask: got pzTransactionId {self.pzTransactionId}')
        logger.debug(f'DeleteTask: got assignment_handle {self.assignment_handle}')
        assert response.status_code == 200 or response.status_code == 303
        return response.text

    async def process_delete(self):
        """
        Processes the delete action using extracted tokens.
        """
        if not self.assignment_handle or not self.pzTransactionId:
            raise Exception("Assignment handle or transaction ID not set.")
        params = {
            "pzTransactionId": self.pzTransactionId,
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "AJAXTrackID": "1",
        }
        data = (
            "pyActivity=ProcessAction"
            f"&$PpyWorkPage$ppyInternalAssignmentHandle={urllib.parse.quote(self.assignment_handle)}"
            "&HarnessType=Review"
            "&Purpose=Review"
            "&NewTaskStatus=DeleteTask"
            "&UITemplatingStatus=Y"
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
        )
        response = await self.async_client.post(
            url=self.pega_url,
            data=data,
            params=params,
            follow_redirects=True
        )
        logger.debug(f'DeleteTask: process_delete status {response.status_code}')
        assert response.status_code == 200
        return response.text

    async def close_task(self):
        """
        Finalizes the deletion by closing the task in the UI.
        """
        params = {
            "pyActivity": "DoClose",
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "pyRemCtlExpProp": "true",
            "pzHarnessID": self.pzHarnessID,
            "AJAXTrackID": "2",
            "retainLock": "false",
            "dcCleanup": "true"
        }
        # Use the original details_url or fallback to a STANDARD url if needed
        url = self.details_url or self.base_url.replace("DCSPA_YardCoordinator", "STANDARD")
        response = await self.async_client.get(
            url=url,
            params=params,
            follow_redirects=True
        )
        logger.debug(f'DeleteTask: close_task status {response.status_code}')
        assert response.status_code == 200
        return response.text

    async def delete_task(self):
        """
        Executes the full delete sequence for the task.
        """
        await self.open_task()
        await self.process_delete()
        await self.close_task()
        logger.info(f"Task {self.task_id} deleted successfully.")
