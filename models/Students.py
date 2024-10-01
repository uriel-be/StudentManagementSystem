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
        self.__students_db = CONFIG["db"]["db_name"]
        self.__students_tbl = 'students'

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
            self.__connection.insert(students, self.__students_db, self.__students_tbl)
            self.__logger.info(f'student {students[0]} added successfully')
        except Exception as err:
            self.__logger.error(traceback.format_exc())
            raise err

    def get_students(self, student_id: int = None
                     , min_age: int = None
                     , max_age: int = None
                     , name: str = None
                     , gender: Gender = None
                     , limit=None
                     ):
        base_query = f'select * from {self.__students_db}.{self.__students_tbl}'
        filters = ' where 1=1'
        if student_id is not None:
            filters += f'and id = {student_id}'
        if name is not None:
            filters += f" and name='{name}'"
        if None not in (max_age, min_age):
            filters += f' and age between {min_age} and {max_age}'
        elif max_age is not None:
            filters += f' and age<{max_age}'
        elif min_age is not None:
            filters += f' and age > {min_age}'
        if gender is not None:
            filters += f" and upper(gender) = '{gender.name}'"
        limit_rows = f' limit {limit}' if limit is not None else ''
        query = base_query + filters + limit_rows
        try:
            self.__logger.debug(f"query students")
            results = self.__connection.query_df(query)
            self.__logger.debug(f"students queried successfully")
        except Exception as err:
            self.__logger.error(f'failed to query students because: {err}')
            raise err
        return results
