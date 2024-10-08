import logging

import pandas

from config_reader import CONFIG
from mysql_connection import Mysql_connection
from models.Students import Students
from models.Courses import Courses
import logging


def get_enrollment_dict(student_id: int, course_id: int, grade):
    enrollment = {
        "student_id": student_id,
        "course": course_id,
        "grade": grade
    }
    return enrollment


class Enrollments:
    def __init__(self, db_connection: Mysql_connection):
        self.__connect = db_connection
        if not self.__connect.is_connected():
            self.__connect.login()
        self.__logger = logging.getLogger('logger')
        self.__students = Students(self.__connect)
        self.__curses = Courses(self.__connect)
        self.__db_name = CONFIG['db']['db_name']
        self.__tbl_name = 'enrollment'

    def get_enrollments(self, **kwargs) -> pandas.DataFrame:
        """
        This Function Return a Pandas Dataframe of Students and the courses they are enroll to.
        :param kwargs: expect to receive a dict with the next keys:
                        students_ids: list<int> (optional)
                        courses_ids: list<int> (optional)
                the values will be used to filter students and courses with x in [] and y in [].
        :return: Pandas Dataframe
        """
        students = kwargs.get('students_ids')
        courses = kwargs.get("courses_ids")
        query = f'''
            select 
                 enrollments.student_id,name,age,contact_info,
                 enrollments.course_id,course_name,grade
            from {self.__db_name}.{self.__tbl_name} enrollments
            join {self.__db_name}.students students
            on enrollments.student_id= students.id
            join {self.__db_name}.courses courses
            on enrollments.course_id = courses.id
        '''
        if students or courses:
            students = f'enrollments.student_id in ({",".join([str(item) for item in students])})' if students else None
            courses = f'enrollments.course_id in ({",".join([str(item) for item in courses])})' if courses else None
            filters = " and ".join(filter(None, [students, courses]))
            query = ' '.join([query, 'where', filters])
        self.__logger.info(f'try to get enrollments list with query: {query}')
        results = self.__connect.query_df(query)
        self.__logger.info(f'{results.count()} enrollments returned.')
        return results

    def is_enrolled(self, student_id: int, course: int) -> bool:
        filters = {
            'students_ids': [student_id],
            'courses_ids': [course]
        }
        result = self.get_enrollments(**filters)
        return result.count() > 0

    def add_enrollment(self, student_id: int, course_id: int):
        if not self.__students.is_student_exist(student_id):
            self.__logger.error("can't add enrollment because student not exist.")
            raise ValueError("can't add enrollment because student not exist.")
        if not self.__curses.is_course_exist(course_id):
            self.__logger.error("can't add enrollment because course not exist.")
            raise ValueError("can't add enrollment because course not exist.")
        enrollment = get_enrollment_dict(student_id, course_id, None)
