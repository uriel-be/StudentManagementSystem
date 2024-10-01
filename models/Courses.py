import logging
from config_reader import CONFIG
from mysql_connection import Mysql_connection


class Courses:
    def __init__(self, db_connection: Mysql_connection):
        self.__connection = db_connection
        if not self.__connection.is_connected():
            self.__connection.login()
        self.__logger = logging.getLogger('logger')
        self.__students_db = CONFIG["db"]["db_name"]
        self.__students_tbl = 'students'

    def __get_course_dict(self, name: str, description: str) -> dict:
        course = {
            'course_name': name
            , 'description': description
        }
        self.__logger.debug(f'course dict created: {course}')
        return course

    def add_course(self, name: str, description: str):
        course = self.__get_course_dict(name, description)
        courses = [course]
        self.add_courses(courses)

    def add_courses(self, courses: list):
        pass
