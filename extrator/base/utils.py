import logging
from ..settings import LOGGER_FORMAT, LOGGER_LEVEL
from sqlalchemy.orm import sessionmaker

engine = {'connection': None}
engine_cx = {'connection': None}


def set_log():
    logging.basicConfig(
        format=LOGGER_FORMAT,
        level=LOGGER_LEVEL)


def logger():
    logger = logging.getLogger('robotj.logger')

    return logger


def conn():
    return engine['connection']


def session():
    if not ('session' in engine and engine['session']):
        engine['session'] = sessionmaker(bind=conn())

    return engine['session']()


def cxoracle():
    return engine_cx['connection']
