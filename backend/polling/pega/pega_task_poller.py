import asyncio
from os import getenv

from dotenv import load_dotenv

from backend.colored_logger import setup_logger
from backend.polling.pega.pega_task_session_manager import PegaTaskSessionManager

logger = setup_logger()
load_dotenv()


class PollingError(Exception):
    """Raised when polling encounters an issue."""
    pass


class PegaTaskPoller:
    def __init__(self, pega_task_session_manager: PegaTaskSessionManager):
        self.pega_task_session_manager = pega_task_session_manager
        self.polling_interval = float(getenv('PEGA_POLLING_INTERVAL', 60))  # default to 60s if not set
        self.polling_task = None
        self.stop_event = asyncio.Event()

    async def poll_hostler_details(self):
        try:
            while not self.stop_event.is_set():
                logger.debug("Starting poll cycle via PegaTaskSessionManager...")

                # 1. Check if re-login is needed
                if self.pega_task_session_manager.should_relogin(max_age_hours=11):
                    logger.info("Session older than 11 hours, performing re-login...")
                    await self.pega_task_session_manager.login()

                # 2. Now fetch
                try:
                    await self.pega_task_session_manager.fetch_all_pega_tasks()
                except Exception as e:
                    logger.error(f"Error during fetching hostler details: {e}")

                logger.info("Poll cycle completed.")

                # 3. Wait for the next cycle or until stop_event is set
                try:
                    await asyncio.wait_for(self.stop_event.wait(), timeout=self.polling_interval)
                except asyncio.TimeoutError:
                    pass  # Means the timeout happened, so do another cycle

        except asyncio.CancelledError:
            logger.info("Polling task canceled.")
        except Exception as e:
            logger.error(f"Unexpected error during polling: {e}")
            raise PollingError("Polling encountered an issue.") from e

    async def start_polling(self):
        """
        Start the polling task. Also do an initial login if needed.
        """
        # Wait 10 seconds to give the websocket time to connect
        await asyncio.sleep(10)
        # If not logged in or older than 11 hours, do an initial login
        if self.pega_task_session_manager.should_relogin():
            logger.info("Session not logged in or older than 11 hours. Logging in now...")
            await self.pega_task_session_manager.login()

        if self.polling_task:
            logger.warning("Polling task is already running.")
            return
        self.polling_task = asyncio.create_task(self.poll_hostler_details())
        logger.info("Polling task started.")

    def stop_polling(self):
        if self.polling_task:
            self.stop_event.set()
            self.polling_task.cancel()
            logger.info("Polling task stopped.")
        else:
            logger.warning("No polling task is running.")

