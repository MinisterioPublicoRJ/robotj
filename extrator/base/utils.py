import logging
from ..settings import LOGGER_FORMAT, LOGGER_LEVEL

engine = {'connection': None}


def conn():
    return engine['connection']


def set_log():
    logging.basicConfig(
        format=LOGGER_FORMAT,
        level=LOGGER_LEVEL)


def logger():
    logger = logging.getLogger('robotj.logger')

    return logger
