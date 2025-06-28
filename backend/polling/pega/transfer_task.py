from backend.colored_logger import setup_logger

from backend.polling.pega.transfer.transfer_from_hostler_to_workbasket import TransferFromHostlerToWorkbasket
from backend.polling.pega.transfer.transfer_from_workbasket_to_hostler import TransferFromWorkbasketToHostler

logger = setup_logger(__name__)


class TransferTask:
    """
    Transfers a task between workbasket and hostler (checker) in Pega.
    If assigned_to is None, transfers from hostler to workbasket.
    If assigned_to is a checker id, transfers from workbasket to hostler.
    """

    def __init__(
            self,
            task_id,
            assigned_to,
            **kwargs
    ):
        """
        :param task_id: The task/case id (e.g. T-34246622)
        :param assigned_to: The checker/user id (e.g. 222982) or None for workbasket transfer
        :param kwargs: additional keys needed for advanced flows (row_page, base_ref, etc)
        """
        self.task_id = task_id
        self.assigned_to = assigned_to
        self.extra = kwargs

        # Session context (set later via set_pega_data)
        self.base_url = None
        self.pzHarnessID = None
        self.pzTransactionId = None
        self.async_client = None
        self.details_url = None

    def set_pega_data(
            self,
            base_url=None,
            pzHarnessID=None,
            pzTransactionId=None,
            async_client=None,
            details_url=None
    ):
        self.base_url = base_url
        self.pzHarnessID = pzHarnessID
        self.pzTransactionId = pzTransactionId
        self.async_client = async_client
        self.details_url = details_url

    async def transfer(self):
        if self.assigned_to:
            # Workbasket → Hostler
            row_page = self.extra.get("row_page")
            base_ref = self.extra.get("base_ref")
            if row_page and base_ref:
                # Advanced workflow
                transfer = TransferFromHostlerToWorkbasket(
                    task_id=self.task_id,
                    checker_id=self.assigned_to,
                    row_page=row_page,
                    base_ref=base_ref
                )
                transfer.set_pega_data(
                    base_url=self.base_url,
                    pzHarnessID=self.pzHarnessID,
                    pzTransactionId=self.pzTransactionId,
                    async_client=self.async_client,
                )
                return await transfer.transfer(
                    fetch_worklist_pd_key=self.extra.get("fetch_worklist_pd_key"),
                    team_members_pd_key=self.extra.get("team_members_pd_key"),
                    section_id_list=self.extra.get("section_id_list"),
                    pzuiactionzzz=self.extra.get("pzuiactionzzz"),
                )
            else:
                # Simple GET-based transfer
                transfer = TransferFromWorkbasketToHostler(
                    task_id=self.task_id,
                    checker_id=self.assigned_to
                )
                transfer.set_pega_data(
                    base_url=self.base_url,
                    pzHarnessID=self.pzHarnessID,
                    async_client=self.async_client,
                    details_url=self.details_url,
                )
                return await transfer.transfer()
        else:
            # Hostler → Workbasket
            row_page = self.extra.get("row_page")
            base_ref = self.extra.get("base_ref")
            if not (row_page and base_ref):
                raise ValueError("row_page and base_ref are required for hostler → workbasket transfer.")
            transfer = TransferFromHostlerToWorkbasket(
                task_id=self.task_id,
                checker_id=None,
                row_page=row_page,
                base_ref=base_ref
            )
            transfer.set_pega_data(
                base_url=self.base_url,
                pzHarnessID=self.pzHarnessID,
                pzTransactionId=self.pzTransactionId,
                async_client=self.async_client,
            )
            return await transfer.transfer(
                fetch_worklist_pd_key=self.extra.get("fetch_worklist_pd_key"),
                team_members_pd_key=self.extra.get("team_members_pd_key"),
                section_id_list=self.extra.get("section_id_list"),
                pzuiactionzzz=self.extra.get("pzuiactionzzz"),
            )
