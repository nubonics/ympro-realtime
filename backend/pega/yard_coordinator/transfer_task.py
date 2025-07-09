from redis.asyncio import Redis

from backend.modules.colored_logger import setup_logger
from backend.modules.storage import get_checker_id_by_name
from backend.pega.yard_coordinator.transfer.transfer_from_hostler_to_workbasket import TransferFromHostlerToWorkbasket
from backend.pega.yard_coordinator.transfer.transfer_from_workbasket_to_hostler import TransferFromWorkbasketToHostler

logger = setup_logger(__name__)


class TransferTask:
    """
    Transfers a task between workbasket and hostler (checker) in Pega.
    If assigned_to is None, transfers from hostler to workbasket.
    If assigned_to is a checker id, transfers from workbasket to hostler.
    """

    def __init__(
            self,
            case_id,
            assigned_to,
            session_manager,
            **kwargs
    ):
        """
        :param task_id: The task/case id (e.g. T-34246622)
        :param assigned_to: The checker/user id (e.g. 222982) or None for workbasket transfer
        :param kwargs: additional keys needed for advanced flows (row_page, base_ref, etc)
        """
        self.extra = kwargs

        self.case_id = case_id
        self.assigned_to = assigned_to
        self.session_manager = session_manager
        self.base_url = self.session_manager.base_url
        self.pzHarnessID = self.session_manager.pzHarnessID
        self.pzTransactionId = self.session_manager.pzTransactionId
        self.async_client = self.session_manager.async_client

    async def transfer(self, redis: Redis):
        assigned_to = (self.assigned_to or "").strip().lower()
        if assigned_to in ("", "workbasket", None):
            # Hostler → Workbasket
            row_page = self.extra.get("row_page")
            base_ref = self.extra.get("base_ref")
            if not (row_page and base_ref):
                raise ValueError("row_page and base_ref are required for hostler → workbasket transfer.")
            transfer = TransferFromHostlerToWorkbasket(
                case_id=self.case_id,
                checker_id=None,
                session_manager=self.session_manager,
                fetch_worklist_pd_key=self.extra.get("fetch_worklist_pd_key"),
                team_members_pd_key=self.extra.get("team_members_pd_key"),
                section_id_list=self.extra.get("section_id_list"),
                pzuiactionzzz=self.extra.get("pzuiactionzzz"),
                row_page=row_page,
                base_ref=base_ref,
                context_page=self.extra.get("context_page") or base_ref or row_page,
                strIndexInList=self.extra.get("strIndexInList") or 'l' + base_ref.split('(')[1].split(')')[0] or 'l' + row_page.split('(')[1].split(')')[0],
                activity_params=self.extra.get("activity_params"),
            )
            return await transfer.transfer()
        else:
            # Workbasket → Hostler
            checker_id = self.assigned_to
            if not checker_id.isdigit():
                checker_id_lookup = await get_checker_id_by_name(redis, checker_id.lower())
                if not checker_id_lookup:
                    raise ValueError(f"Could not resolve checker id for hostler name '{checker_id}'")
                checker_id = checker_id_lookup

            # Regardless of row_page/base_ref, use TransferFromWorkbasketToHostler!
            transfer = TransferFromWorkbasketToHostler(
                case_id=self.case_id,
                checker_id=checker_id,
                session_manager=self.session_manager,
            )
            return await transfer.transfer()
