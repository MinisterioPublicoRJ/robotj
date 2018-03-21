import logging
from ..settings import LOGGER_FORMAT

engine = {'connection': None}


def conn():
    return engine['connection']


def set_log():
    logging.basicConfig(format=LOGGER_FORMAT)


def logger():
    logger = logging.getLogger('robotj.logger')
    return logger
