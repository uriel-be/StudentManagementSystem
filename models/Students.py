import logging
import traceback
import mysql_connection
from enums.Gender import Gender


class Students:
    def __init__(self, db_connection: mysql_connection):
        self.__connection = db_connection
        self.__connection.login()
        self.__logger = logging.getLogger('logger')

    def create_student(self, full_name: str, age: int, gender: Gender, contact_info: str):
        if age < 10 or age > 100:
            msg = f'can\'t insert {full_name} because age not between 10 and 100'
            self.__logger.error(msg)
            raise ValueError(traceback.format_exc())
        self.__connection.query(
            f'insert into StudentManagement.students values ({full_name},{age},{gender.name},{contact_info})')
