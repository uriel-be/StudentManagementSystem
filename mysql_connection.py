import mysql.connector as connector
import mysql.connector.errors
import logging

import pandas as pandas


class Mysql_connection:
    def __init__(self, hostname, port=3306):
        self.__is_connected = False
        self.__connection = None
        self.__logger = logging.getLogger("mysql_connection")
        self.hostname = hostname
        self.port = port

    def is_connected(self):
        return self.__is_connected

    def get_connection(self):
        return self.__connection

    def login(self, username: str, password: str):
        try:
            self.__connection = connector.connect(
                host=self.hostname,
                port=self.port,
                username=username,
                password=password
            )
            if self.__connection.is_connected():
                self.__is_connected = True
                self.__logger.info(f"connected to db {self.hostname}:{self.port}")
        except mysql.connector.errors.DatabaseError as err:
            self.__logger.fatal(err.msg)
            raise mysql.connector.errors.DatabaseError(err.msg)

    def query(self, query: str, params: tuple = None):
        """
            execute and return query answer. \n
            input:
                1.query:str -sql query \n
                2.params:tuple (optional) - a tuple of params to set in the sql query.
            this func return:
                1. data:list<tuples> - any tuple in the list is a row in DB
                2.column_names : list
            errors-
             mysql.connector.errors.DatabaseError - this will be rais if db not connected. \n
             mysql.connector.errors.ProgrammingError -this will be rais if db not exists or query is incorrect.\n
        """
        if not self.__is_connected:
            self.__logger.error(f'{query}; can not be executed because db not connected')
            raise mysql.connector.errors.DatabaseError(f'{query}; can not be executed because db not connected')
        curser = self.__connection.cursor()
        try:
            curser.execute(query, params)
            result = curser.fetchall()
            self.__logger.info(f'The query "{curser.statement}" return {curser.rowcount} rows')
            return result, list(curser.column_names)
        except mysql.connector.errors.ProgrammingError as err:
            self.__logger.error(err)
            raise err
        except Exception as err:
            self.__logger.error(err)
            raise err

    def query_df(self, sql_query: str, params: tuple = None):
        result, columns = self.query(sql_query, params)
        if not result:
            return None
        df = pandas.DataFrame(data=result, columns=columns)
        print(df)
