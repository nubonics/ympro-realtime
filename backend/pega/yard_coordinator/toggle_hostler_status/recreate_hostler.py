import logging

from backend.pega.yard_coordinator.toggle_hostler_status.create_hostler import CreateHostler
from backend.pega.yard_coordinator.toggle_hostler_status.delete_hostler import DeleteHostler

logger = logging.getLogger(__name__)


class ToggleHostlerStatus:
    """
    Orchestrates the hostler delete and re-create sequence.
    """

    def __init__(self, session_manager, hostler):
        self.session_manager = session_manager
        self.hostler = hostler
        self.delete_workflow = DeleteHostler(session_manager, hostler)
        self.create_workflow = CreateHostler(session_manager, hostler)

    async def run(self):
        # Run delete, capturing pzuiactionzzz for create
        step7_pzuiactionzzz = await self.delete_workflow.run()
        # Run create, passing along the pzuiactionzzz discovered
        await self.create_workflow.run(step7_pzuiactionzzz)
        logger.info("ToggleHostlerStatus flow completed.")
