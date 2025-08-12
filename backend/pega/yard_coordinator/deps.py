import asyncio
from os import getenv
from dotenv import load_dotenv

from redis.asyncio import Redis

from backend.modules.colored_logger import setup_logger
from backend.pega.yard_coordinator.session_manager.manager import PegaTaskSessionManager
from backend.modules.storage import set_latest_poll_result, cleanup_expired_tasks
from backend.rules.validation import validate_and_store_tasks
from enum import Enum, auto
from backend.modules.tasks_hub import tasks_hub  # WS hub broadcaster

logger = setup_logger()
load_dotenv()

MERGED_POLL_INTERVAL = float(getenv('PEGA_POLLING_INTERVAL', 60))  # seconds


class PollingError(Exception):
    """Raised when polling encounters an issue."""
    pass


class PollerState(Enum):
    STOPPED = auto()
    RUNNING = auto()
    STOPPING = auto()
    ERROR = auto()


class PegaTaskPoller:
    def __init__(self, pega_task_session_manager: PegaTaskSessionManager, redis: Redis, handle_payload=None):
        self.pega_task_session_manager = pega_task_session_manager
        self.redis = redis
        self.polling_interval = MERGED_POLL_INTERVAL
        self.polling_task = None
        self.stop_event = asyncio.Event()
        self.handle_payload = handle_payload
        self.state = PollerState.STOPPED
        self._last_error = None

    @property
    def is_running(self):
        return self.state == PollerState.RUNNING

    @property
    def has_error(self):
        return self.state == PollerState.ERROR

    @property
    def last_error(self):
        return self._last_error

    async def poll_pega(self):
        self.state = PollerState.RUNNING
        self._last_error = None
        try:
            while not self.stop_event.is_set():
                logger.debug("Starting poll cycle via PegaTaskPoller...")

                try:
                    # 1. Check if re-login is needed
                    if self.pega_task_session_manager.should_relogin(max_age_hours=11):
                        logger.info("Session older than 11 hours, performing re-login...")
                        await self.pega_task_session_manager.login()
                except Exception as e:
                    logger.error(f"Error during session check or login: {e}")
                    raise PollingError("Failed to check session or login.") from e

                # 2. Fetch all tasks from Pega
                try:
                    await self.pega_task_session_manager.fetch_all_pega_tasks()
                except Exception as e:
                    logger.error(f"Error during fetching tasks from Pega: {e}")

                try:
                    # 3. Get all parsed tasks from the task store
                    all_task_dicts = await self.pega_task_session_manager.task_store.get_all_tasks()
                except Exception as e:
                    logger.error(f"Error fetching tasks from task store: {e}")
                    all_task_dicts = []

                try:
                    # 4. Validate and store tasks (returns only valid tasks, deletes unwanted)
                    valid_tasks = await validate_and_store_tasks(
                        all_task_dicts, self.pega_task_session_manager.task_store,
                        session_manager=self.pega_task_session_manager
                    )
                except Exception as e:
                    logger.error(f"Error validating and storing tasks: {e}")
                    valid_tasks = []

                unwanted_count = len(all_task_dicts) - len(valid_tasks)

                try:
                    # 5. Store only valid tasks in Redis AND broadcast over WS (same snapshot)
                    serialized_tasks = [
                        t.model_dump() if hasattr(t, "model_dump") else t
                    for t in valid_tasks
                    ]
                    await set_latest_poll_result(serialized_tasks, self.redis)

                    # ---> WS push (no Pub/Sub; single-process)
                    await tasks_hub.set_snapshot(serialized_tasks)

                    # Optional custom handler
                    if self.handle_payload is not None:
                        await self.handle_payload(valid_tasks, self.redis)

                except Exception as e:
                    logger.error(f"Error storing/broadcasting valid tasks: {e}")
                    raise PollingError("Failed to store or broadcast valid tasks.") from e

                try:
                    # 6. Log counts
                    logger.info(
                        f"Poll cycle: {len(valid_tasks)} valid tasks, {unwanted_count} unwanted (deleted) tasks, poll interval={self.polling_interval}s"
                    )
                except Exception as e:
                    logger.error(f"Error logging counts: {e}")

                try:
                    await cleanup_expired_tasks(self.redis)
                except Exception as e:
                    logger.error(f"Error during cleanup of expired tasks: {e}")

                # Wait for next cycle
                try:
                    await asyncio.wait_for(self.stop_event.wait(), timeout=self.polling_interval)
                except asyncio.TimeoutError:
                    pass  # Continue polling

        except asyncio.CancelledError:
            self.state = PollerState.STOPPED
            logger.info("Polling task canceled.")
        except Exception as e:
            self._last_error = e
            self.state = PollerState.ERROR
            logger.error(f"Unexpected error during polling: {e}")
            raise PollingError("Polling encountered an issue.") from e
        finally:
            if self.state != PollerState.ERROR:
                self.state = PollerState.STOPPED

    async def start_polling(self):
        if self.is_running:
            logger.warning("Polling task is already running.")
            return
        if self.polling_task and not self.polling_task.done():
            logger.warning("Polling task is still running in background.")
            return
        if self.has_error:
            logger.warning(f"Polling previously stopped due to error: {self.last_error}. Resetting state and restarting.")
        self.stop_event.clear()  # Reset the event before starting
        self.state = PollerState.STOPPED  # Reset state before starting
        await asyncio.sleep(5)  # Optional: let websockets connect etc
        if self.pega_task_session_manager.should_relogin():
            logger.info("Session not logged in or older than 11 hours. Logging in now...")
            await self.pega_task_session_manager.login()
        self.polling_task = asyncio.create_task(self.poll_pega())
        logger.info("Polling task started.")

    def stop_polling(self):
        if not self.is_running:
            logger.warning("Polling is not running.")
            return
        self.state = PollerState.STOPPING
        self.stop_event.set()
        if self.polling_task:
            self.polling_task.cancel()
        logger.info("Polling task stop requested.")

    def get_state(self):
        return self.state.name

    def get_status(self):
        return {
            "state": self.state.name,
            "is_running": self.is_running,
            "has_error": self.has_error,
            "last_error": str(self.last_error) if self.has_error else None,
        }


def get_pega_poller(app):
    return app.state.pega_poller
