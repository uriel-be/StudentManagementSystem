from mysql_connection import Mysql_connection
from logger import build_logger
from config_reader import config_read
from config_reader import CONFIG
import os

def setup(logs_dir):
    build_logger(logs_dir)
    config_read()


if __name__ == '__main__':
    setup('./logs')
    con = Mysql_connection(CONFIG["db"]["hostname"], CONFIG["db"]["port"])
    con.login(CONFIG["db"]["username"], CONFIG["db"]["password"])


