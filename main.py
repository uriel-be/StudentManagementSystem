from models.Students import Students
from mysql_connection import Mysql_connection
from logger import build_logger
from config_reader import config_read
from config_reader import CONFIG
from enums.Gender import Gender
from models.Courses import Courses

import os


def setup(logs_dir):
    build_logger(logs_dir)
    config_read()


if __name__ == '__main__':
    setup('./logs')
    con = Mysql_connection(CONFIG["db"]["hostname"], CONFIG["db"]["username"],
                           CONFIG["db"]["password"], CONFIG["db"]["port"])
    con.login()
    # data, columns = con.query('select * from StudentManagement.students')
    # stud = Students(con)
    # print(stud.get_students(gender=Gender.MALE))
    courses = Courses(con)
    # courses.add_course('some course', 'description')
    courses.get_courses(**{"ids": [1, 2, 3, 4, 5], "limit": 10})
