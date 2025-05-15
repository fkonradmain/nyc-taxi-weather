import logging
import sys
from typing import TextIO

from .config import Config

__name__ = "logger"

# Get default logger
logger: logging.Logger = logging.getLogger("kestra-group-sync")

# Create formatter
formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")

# Create logging handlers
stream_handler: logging.StreamHandler[TextIO] = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

# Add handler to logger
logger.handlers = [stream_handler]

logger.setLevel(Config.LOG_LEVEL)
logger.info("LOG LEVEL: %s", Config.LOG_LEVEL)
