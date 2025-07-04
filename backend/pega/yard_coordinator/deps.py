import asyncio
from os import getenv
from dotenv import load_dotenv

from redis.asyncio import Redis

from backend.modules.colored_logger import setup_logger
from backend.pega.yard_coordinator.session_manager.manager import PegaTaskSessionManager
from backend.modules.storage import set_latest_poll_result

logger = setup_logger()
load_dotenv()

MERGED_POLL_INTERVAL = float(getenv('PEGA_POLLING_INTERVAL', 60))  # seconds


class PollingError(Exception):
    """Raised when polling encounters an issue."""
    pass


class PegaTaskPoller:
    def __init__(self, pega_task_session_manager: PegaTaskSessionManager, redis: Redis, handle_payload=None):
        self.pega_task_session_manager = pega_task_session_manager
        self.redis = redis
        self.polling_interval = MERGED_POLL_INTERVAL
        self.polling_task = None
        self.stop_event = asyncio.Event()
        self.handle_payload = handle_payload

    async def poll_pega(self):
        try:
            while not self.stop_event.is_set():
                logger.debug("Starting poll cycle via PegaTaskPoller...")

                # 1. Check if re-login is needed
                if self.pega_task_session_manager.should_relogin(max_age_hours=11):
                    logger.info("Session older than 11 hours, performing re-login...")
                    await self.pega_task_session_manager.login()

                # 2. Fetch all tasks from Pega (this will apply all validation & business rules)
                try:
                    await self.pega_task_session_manager.fetch_all_pega_tasks()
                except Exception as e:
                    logger.error(f"Error during fetching tasks from Pega: {e}")

                # 3. Get only the valid tasks from the task store
                raw_tasks = await self.pega_task_session_manager.task_store.get_all_tasks()
                # These should already be valid thanks to centralized validation
                # You can optionally convert to your Task model here if needed

                # 4. Publish to Redis or notify handlers
                await set_latest_poll_result([t.model_dump() if hasattr(t, "model_dump") else t for t in raw_tasks],
                                             self.redis)
                if self.handle_payload is not None:
                    await self.handle_payload(raw_tasks, self.redis)

                logger.info(f"Poll cycle: {len(raw_tasks)} valid tasks, poll interval={self.polling_interval}s")

                # Wait for next cycle
                try:
                    await asyncio.wait_for(self.stop_event.wait(), timeout=self.polling_interval)
                except asyncio.TimeoutError:
                    pass  # Continue polling

        except asyncio.CancelledError:
            logger.info("Polling task canceled.")
        except Exception as e:
            logger.error(f"Unexpected error during polling: {e}")
            raise PollingError("Polling encountered an issue.") from e

    async def start_polling(self):
        await asyncio.sleep(5)  # Optional: let websockets connect etc
        if self.pega_task_session_manager.should_relogin():
            logger.info("Session not logged in or older than 11 hours. Logging in now...")
            await self.pega_task_session_manager.login()
        if self.polling_task:
            logger.warning("Polling task is already running.")
            return
        self.polling_task = asyncio.create_task(self.poll_pega())
        logger.info("Polling task started.")

    def stop_polling(self):
        if self.polling_task:
            self.stop_event.set()
            self.polling_task.cancel()
            logger.info("Polling task stopped.")
        else:
            logger.warning("No polling task is running.")


def get_pega_poller(app):
    return app.state.pega_poller
