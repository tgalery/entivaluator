import logging
import os
import sys

_LOGGER_NAME = "entivaluator"
_BASE_PATH = os.path.realpath(__file__).split("utils")[0]


def get_logger():
    """
    A function for getting a logger instance
    """

    formatter = logging.Formatter(fmt='%(asctime)s : %(levelname)s : %(message)s')
    logger = logging.getLogger(_LOGGER_NAME)
    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.setLevel(logging.INFO)
    return logger
