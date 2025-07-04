from os import makedirs
from os.path import exists

from backend.modules.colored_logger import setup_logger

logger = setup_logger(__name__)


def save_html_to_file(content, step: int, enabled: bool = False):
    if not enabled:
        return
    if enabled is False:
        return
    try:
        file_path = f"debug_html/step_{step}.html"
        if not exists("debug_html"):
            makedirs("debug_html", exist_ok=True)
        if isinstance(content, str):
            content = content.encode("utf-8")
        with open(file_path, "wb") as file:
            file.write(content)
        logger.debug(f"Saved HTML content for step {step} to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save HTML content for step {step}: {e}")
