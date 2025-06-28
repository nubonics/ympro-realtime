import logging
import colorlog


def setup_logger(name: str = None):
    """
    Set up a colored logger for the application.
    """
    log_colors = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False  # Disable propagation to avoid duplicate logs

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s[%(asctime)s] [%(levelname)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors=log_colors,
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
