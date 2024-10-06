import logging
from config_reader import CONFIG
from mysql_connection import Mysql_connection


class Courses:
    def __init__(self, db_connection: Mysql_connection):
        self.__connection = db_connection
        if not self.__connection.is_connected():
            self.__connection.login()
        self.__logger = logging.getLogger('logger')
        self.__courses_db = CONFIG["db"]["db_name"]
        self.__courses_tbl = 'courses'

    def __get_course_dict(self, name: str, description: str) -> dict:
        course = {
            'course_name': name,
            'description': description
        }
        self.__logger.debug(f'course dict created: {course}')
        return course

    def add_course(self, name: str, description: str):
        course = self.__get_course_dict(name, description)
        courses = [course]
        self.add_courses(courses)

    def add_courses(self, courses: list):
        if not courses:
            self.__logger.info('not fount courses to add')
            return
        self.__logger.info(f'try to add {len(courses)} new courses')
        self.__connection.insert(courses, self.__courses_db, self.__courses_tbl)

    def get_courses(self, **kwargs):
        """
        this function return a Pandas DF with details about courses.
        :param kwargs: expect to dict with the keys:
                        ids:list (optional key),
                        names:list (optional key),
                        limit:int (optional key)
                        they will use to filter in the query.
                        example:{'ids':[1,2,3],'names':[],limit:10}
        :return: Pandas DF of courses
        """
        ids = kwargs.get('ids')
        names = kwargs.get('names')
        limit = kwargs.get('limit')
        query = f'select * from {self.__courses_db}.{self.__courses_tbl}'
        if ids or names:
            formatted_id = f"id in ({','.join(str(course_id) for course_id in ids)}) " if ids else None
            formatted_names = f'''course_name in ({','.join(["'" + name + "'" for name in names])}) ''' if names else None
            filters: str = 'and '.join(filter(None, [formatted_names, formatted_id]))
            query += f' where {filters}'
        if limit and type(limit) is int:
            query += f' limit {limit}'
        query += ';'
        self.__logger.info(f'Try get courses list with query: "{query}"')
        result = self.__connection.query_df(query)
        print(result)
