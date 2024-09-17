import logging
import enum
import os


def build_logger(path: str, level: str='DEBUG', file_name='log.log'):
    logger_levels = ['CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG', 'NOTSET']
    if level.upper() not in logger_levels:
        raise ValueError(f'level most be in {logger_levels}')
    if not os.path.exists(path):
        os.mkdir(path)
    logging.basicConfig(filename=f'{path}/{file_name}', encoding='utf-8')
    logging.getLogger('logger').setLevel(level)
