from models.Students import Student
from mysql_connection import Mysql_connection
from logger import build_logger
from config_reader import config_read
from config_reader import CONFIG
from enums.Gender import Gender

import os


def setup(logs_dir):
    build_logger(logs_dir)
    config_read()


if __name__ == '__main__':
    setup('./logs')
    con = Mysql_connection(CONFIG["db"]["hostname"], CONFIG["db"]["username"],
                           CONFIG["db"]["password"], CONFIG["db"]["port"])
    con.login()
    data, columns = con.query('select * from StudentManagement.students')
    print(f'columns: {columns} \n data:{data}')
    query_df = con.query_df('select * from StudentManagement.students')
    data = [{'name': 'abc', 'age': 17, 'gender': Gender.MALE.name, 'contact_info': 'example'},
            {'name': 'bcd', 'age': 'aaa', 'gender': Gender.MALE.name, 'contact_info': 'example'}]
    con.insert(data, 'StudentManagement', 'students')
