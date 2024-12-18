import logging
from colorlog import ColoredFormatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()

formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-8s %(asctime)s %(reset)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        "INFO": "green",
        "ERROR": "red",
    },
)

handler.setFormatter(formatter)

logger.addHandler(handler)
