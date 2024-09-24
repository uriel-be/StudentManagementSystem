import logging
import traceback
import mysql_connection
from enums.Gender import Gender
from config_reader import CONFIG


class Students:
    def __init__(self, db_connection: mysql_connection):
        self.__connection = db_connection
        self.__connection.login()
        self.__logger = logging.getLogger('logger')

    def __create_student_dict(self, full_name: str, age: int, gender: Gender, contact_info: str):
        student = {
            'name': full_name,
            'age': age,
            'gender': gender,
            'contact_info': contact_info
        }
        self.__logger.debug(f'student dict created: {student}')
        return student

    def create_student(self, full_name: str, age: int, gender: Gender, contact_info: str):
        if age < 10 or age > 100:
            msg = f'can\'t insert {full_name} because age not between 10 and 100'
            self.__logger.error(msg)
            raise ValueError(msg)
        try:
            students = [self.__create_student_dict(full_name, age, gender.name, contact_info)]
            self.__logger.info(f'start add student {students[0]}.')
            self.__connection.insert(students, CONFIG["db"]["db_name"], 'students')
            self.__logger.info(f'student {students[0]} added successfully')
        except Exception as err:
            self.__logger.error(traceback.format_exc())
            raise err
