import sys

from models.Students import Students
from mysql_connection import Mysql_connection
from logger import build_logger
from config_reader import config_read
from config_reader import CONFIG
from enums.Gender import Gender
from models.Courses import Courses
from models.Enrollments import Enrollments

import os


def setup(logs_dir):
    build_logger(logs_dir)
    config_read()


if __name__ == '__main__':
    '''
    This app expect to receive 3 param from out:
    1.logger relative path
    2.DB username
    3.DB password
    in this order.
    example how to run: py ./main.py <logger_path> <db_username> <db_password>
    '''
    setup(sys.argv[1])
    con = Mysql_connection(CONFIG["db"]["hostname"], username=sys.argv[2],
                           password=sys.argv[3], port=CONFIG["db"]["port"])
    con.login()
    # data, columns = con.query('select * from StudentManagement.students')
    # stud = Students(con)
    # print(stud.get_students(gender=Gender.MALE))
    courses = Courses(con)
    # courses.add_course('some course', 'description')
    # courses.get_courses(**{"ids": [1, 2, 3, 4, 5], "limit": 10})
    enrollments = Enrollments(con)
    print(enrollments.is_enrolled(80, 5))
