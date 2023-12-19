import logging
import os

from rich.logging import RichHandler

from inference.core.env import LOG_LEVEL

logger = logging.getLogger("inference")
logger.setLevel(LOG_LEVEL)
logger.addHandler(RichHandler())
