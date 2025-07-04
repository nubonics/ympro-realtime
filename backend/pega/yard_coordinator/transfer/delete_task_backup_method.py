import urllib.parse
import time
from lxml import html

from backend.modules.colored_logger import setup_logger
from backend.pega.yard_coordinator.session_manager.debug import save_html_to_file

logger = setup_logger(__name__)

class DeleteTaskManager:
    """
    Handles the multi-step Pega delete task operation using session manager context.
    Call set_pega_data() before using step methods.
    """

    def __init__(self, task_id):
        self.task_id = task_id
        self.async_client = None
        self.base_url = None
        self.pzHarnessID = None
        self.csrf_token = None
        self.fingerprint_token = None
        self.details_url = None
        self.pega_url = None
        self.pzTransactionId = None
        self.assignment_handle = None

    def set_pega_data(self, base_url, pzHarnessID, async_client, csrf_token, fingerprint_token, details_url=None):
        self.base_url = base_url.rstrip('/').replace("DCSPA_YardCoordinator", "STANDARD")
        self.pzHarnessID = pzHarnessID
        self.async_client = async_client
        self.csrf_token = csrf_token
        self.fingerprint_token = fingerprint_token
        self.details_url = details_url
        self.pega_url = self.base_url.replace('STANDARD', 'DCSPA_YardCoordinator')

    @staticmethod
    def _parse_html(html_content):
        try:
            tree = html.fromstring(html_content)
            return tree
        except Exception as e:
            logger.error("Failed to parse HTML: %s", e)
            return None

    # --- Step 1: Open Task ---
    async def open_task(self):
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
        save_html_to_file(content=response.content, step=100)
        logger.debug(f'DeleteTaskManager: open_task status {response.status_code}')
        # You may need to parse pzTransactionId and assignment_handle here as well for later steps
        self.pzTransactionId = self.extract_pzTransactionId(response.content)
        self.assignment_handle = self.extract_assignment_handle(response.content)
        logger.debug(f'DeleteTaskManager: pzTransactionId={self.pzTransactionId}')
        logger.debug(f'DeleteTaskManager: assignment_handle={self.assignment_handle}')
        assert response.status_code in (200, 303)
        return response.text

    # --- Step 2: Run Action Wrapper for Case History ---
    async def run_action_wrapper_case_history(self, instance_id, grid_params, harness_id):
        """
        grid_params: should be a dict with correct keys for your case history grid.
        """
        url = f"{self.pega_url}?pzTransactionId={self.pzTransactionId}&pzFromFrame=pyWorkPage&pzPrimaryPageName=pyWorkPage&AJAXTrackID=1"
        # You may need to build the strJSON and other params exactly as in your requests
        data = (
            f"pyActivity=pzRunActionWrapper"
            f"&strJSON={urllib.parse.quote(grid_params)}"
            f"&instanceId={instance_id}"
            "&pzKeepPageMessages=true"
            "&UITemplatingStatus=N"
            "&inStandardsMode=true"
            f"&pzHarnessID={harness_id}"
            "&pzActivity=pzBuildFilterIcon"
            "&skipReturnResponse=true"
            "&pySubAction=runAct"
        )
        response = await self.async_client.post(url, data=data)
        save_html_to_file(content=response.content, step=110)
        logger.debug(f'DeleteTaskManager: run_action_wrapper_case_history status {response.status_code}')
        assert response.status_code == 200
        return response.text

    # --- Step 3: Reload Section ---
    async def reload_section(self):
        url = f"{self.pega_url}?pzTransactionId={self.pzTransactionId}&pzFromFrame=pyWorkPage&pzPrimaryPageName=pyWorkPage&AJAXTrackID=1"
        data = (
            "pyActivity=ReloadSection"
            # ... (rest of your very long ReloadSection payload) ...
            f"&pzHarnessID={self.pzHarnessID}"
            "&PreActivity=&PreDataTransform="
        )
        response = await self.async_client.post(url, data=data)
        save_html_to_file(content=response.content, step=120)
        logger.debug(f'DeleteTaskManager: reload_section status {response.status_code}')
        assert response.status_code == 200
        return response.text

    # --- Step 4: Process Delete ---
    async def process_delete(self):
        url = f"{self.pega_url}?pzTransactionId={self.pzTransactionId}&pzFromFrame=pyWorkPage&pzPrimaryPageName=pyWorkPage&AJAXTrackID=1"
        data = (
            "pyActivity=ProcessAction"
            f"&$PpyWorkPage$ppyInternalAssignmentHandle={urllib.parse.quote(self.assignment_handle)}"
            "&HarnessType=Review"
            "&Purpose=Review"
            "&UITemplatingStatus=Y"
            "&NewTaskStatus=DeleteTask"
            f"&pzHarnessID={self.pzHarnessID}"
            "&inStandardsMode=true"
        )
        response = await self.async_client.post(url, data=data)
        save_html_to_file(content=response.content, step=130)
        logger.debug(f'DeleteTaskManager: process_delete status {response.status_code}')
        assert response.status_code == 200
        return response.text

    # --- Step 5: Finalize/DoClose ---
    async def close_task(self):
        url = f"{self.base_url}?pyActivity=DoClose&pzFromFrame=pyWorkPage&pzPrimaryPageName=pyWorkPage&pyRemCtlExpProp=true&pzHarnessID={self.pzHarnessID}&AJAXTrackID=1&retainLock=false&dcCleanup=true"
        response = await self.async_client.get(url)
        save_html_to_file(content=response.content, step=140)
        logger.debug(f'DeleteTaskManager: close_task status {response.status_code}')
        assert response.status_code == 200
        return response.text

    # --- Utility extraction methods from your original class ---
    @staticmethod
    def extract_pzTransactionId(html_content):
        tree = html.fromstring(html_content)
        xpath_expr = "//script[contains(text(), 'pega.ui.jittemplate.addMetadataTree')]"
        script_elements = tree.xpath(xpath_expr)
        if not script_elements:
            logger.warning("No script elements found for transaction id extraction")
            return None
        script_text = script_elements[0].text
        import re
        match = re.search(r"pzTransactionId=([^&\"\s]+)", script_text or "")
        return match.group(1) if match else None

    @staticmethod
    def extract_assignment_handle(html_content):
        html_text = html_content.decode() if isinstance(html_content, bytes) else html_content
        from lxml import html as lxml_html
        import re
        # Try input fields
        try:
            tree = lxml_html.fromstring(html_text)
            elems = tree.xpath("//input[@id='assignmentHandle' or @name='assignmentHandle']")
            if elems and elems[0].get('value'):
                return elems[0].get('value')
            # Try data attributes
            elems = tree.xpath("//*[@data-assignmenthandle]")
            if elems and elems[0].get('data-assignmenthandle'):
                return elems[0].get('data-assignmenthandle')
        except Exception as e:
            logger.warning(f"HTML parsing failed for assignment handle extraction: {e}")
        # Fallback regex
        match = re.search(
            r'ASSIGN-INTERNAL\s+ESTES-OPS-YARDMGMT-WORK\s+T-\d+!PZINTERNALCASEFLOW', html_text
        )
        if match:
            return match.group(0)
        logger.warning("Assignment handle not found in HTML content.")
        return None

    # --- Orchestrator ---
    async def delete_task(self):
        await self.open_task()
        # Optionally: run_action_wrapper_case_history and reload_section if required by Pega flow
        await self.process_delete()
        await self.close_task()
        logger.info(f"Task {self.task_id} deleted successfully.")
