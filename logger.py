import logging
import enum
import os


class Level(enum):
    DEBUG = logging.DEBUG,
    INFO = logging.INFO,
    WARN = logging.WARN,
    ERROR = logging.ERROR


def build_logger(path: str, level: Level = Level.DEBUG, file_name='log.log'):
    if not os.path.exists(path):
        os.mkdir(path)
    logging.basicConfig(filename=f'{path}/{file_name}', encoding='utf-8', level=level)
