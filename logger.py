import logging
import enum
import os
import sys

def build_logger(path: str,
                 level: str = 'DEBUG',
                 file_name='log.log',
                 logger_format='%(asctime)s-%(name)s-%(levelname)s- %(message)s'
                 ):
    logger_levels = list(logging._nameToLevel.keys())
    if level.upper() not in logger_levels:
        raise ValueError(f'level most be in {logger_levels}')
    os.makedirs(path,exist_ok=True)
    logging.basicConfig(
        filename=f'{path}/{file_name}',
        encoding='utf-8',
        format=logger_format,
        level=level.upper()
    )
    logging.getLogger('logger').addHandler(logging.StreamHandler(sys.stdout))
