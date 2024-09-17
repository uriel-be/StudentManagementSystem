import json
import logging
import os

CONFIG_PATH = 'config/config.json'


def config_read() -> dict:
    logger = logging.getLogger('config_reader')
    if not os.path.exists(CONFIG_PATH):
        logger.fatal('config.json file not found in config folder.')
        raise FileNotFoundError('config.json file not found.')
    with open(CONFIG_PATH,mode='r') as file:
        try:
            config=json.loads(file.read())
            return config
        except json.decoder.JSONDecodeError as err:
            logger.fatal(err)
            raise err

CONFIG=config_read()