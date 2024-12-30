import os
import sys
from enum import Enum
from loguru import logger


class LogLevels(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


log_formats = {
    LogLevels.DEBUG: (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
        "| <level>{level:<8}</level> "
        "| <cyan>{name}:{function}:{line}</cyan> "
        "- <level>{message}</level>"
    ),
    LogLevels.INFO: (
        "<blue>{time:YYYY-MM-DD HH:mm:ss.SSS}</blue> "
        "| <level>{level:<8}</level> "
        "| <cyan>{name}:{function}:{line}</cyan> "
        "- <level>{message}</level>"
    ),
    LogLevels.WARNING: (
        "<yellow>{time:YYYY-MM-DD HH:mm:ss.SSS}</yellow> "
        "| <level>{level:<8}</level> "
        "| <cyan>{name}:{function}:{line}</cyan> "
        "- <level>{message}</level>"
    ),
    LogLevels.ERROR: (
        "<red>{time:YYYY-MM-DD HH:mm:ss.SSS}</red> "
        "| <level>{level:<8}</level> "
        "| <cyan>{name}:{function}:{line}</cyan> "
        "- <level>{message}</level>"
    ),
    LogLevels.CRITICAL: (
        "<red><b>{time:YYYY-MM-DD HH:mm:ss.SSS}</b></red> "
        "| <level>{level:<8}</level> "
        "| <cyan>{name}:{function}:{line}</cyan> "
        "- <level>{message}</level>"
    ),
}


def configure_logger(
    console_level: LogLevels = LogLevels.DEBUG,
    traceback_level: LogLevels = LogLevels.ERROR
) -> None:
    """
    - Sends colorized logs of 'console_level' and above to console.
    - Sends traceback logs of 'traceback_level' and above to files in logs/tracebacks.
    """
    logger.remove()

    os.makedirs("logs/tracebacks", exist_ok=True)

    logger.add(
        sys.stderr,
        level=console_level.value,
        format=log_formats[console_level],
        colorize=True,
        backtrace=False,
        diagnose=False
    )

    logger.add(
        "logs/tracebacks/tracebacks_{time}.log",
        level=traceback_level.value,
        format=log_formats[traceback_level],
        rotation="1 week",
        backtrace=True,
        diagnose=True
    )
