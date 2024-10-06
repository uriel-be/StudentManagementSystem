import mysql.connector as connector
import mysql.connector.errors
import logging
import traceback

import pandas as pandas


class Mysql_connection:
    def __init__(self, hostname, username: str, password: str, port=3306):
        self.__is_connected = False
        self.__connection = None
        self.__logger = logging.getLogger("mysql_connection")
        self.hostname = hostname
        self.port = port
        self.__username = username
        self.__pass = password

    def is_connected(self):
        return self.__is_connected

    def get_connection(self):
        return self.__connection

    def __get_cursor(self):
        if not self.__is_connected:
            self.__logger.error(f'can not create cursor because db not connected.')
            raise mysql.connector.errors.DatabaseError(f'can not create cursor because db not connected.')
        return self.__connection.cursor()

    def login(self):
        try:
            self.__connection = connector.connect(
                host=self.hostname,
                port=self.port,
                username=self.__username,
                password=self.__pass
            )
            if self.__connection.is_connected():
                self.__is_connected = True
                self.__logger.info(f"connected to db {self.hostname}:{self.port}")
        except mysql.connector.errors.DatabaseError as err:
            self.__logger.fatal(traceback.format_exc())
            raise mysql.connector.errors.DatabaseError(traceback.format_exc())

    def insert(self, values: list, db_name: str, table: str):
        """
        :param values:list of object. any object is in format ColumnName:Value
        :param db_name:str DB name
        :param table:str table name
        """
        all_values = []
        cols = []
        for val in values:
            new_values = []
            for col_val in val.values():
                if col_val is None:
                    new_values.append('null')
                elif str(col_val).isnumeric():
                    new_values.append(str(col_val))
                else:
                    new_values.append(f"'{col_val}'")
            all_values.append(f'({",".join(new_values)})')
            if not cols:
                cols = val.keys()
        insert_query = f'insert into {db_name}.{table} ({",".join(cols)}) values {",".join(all_values)}'
        try:
            self.__logger.debug(f'running query:"{insert_query}"')
            cursor = self.__get_cursor()
            cursor.execute(insert_query)
            self.__connection.commit()
            self.__logger.info(f'{cursor.rowcount} rows inserted into {db_name}.{table}.')
        except Exception as err:
            self.__logger.error(traceback.format_exc())
            raise err

    def query(self, query: str, params: tuple = None):
        """
            execute and return query answer. \n
            :param: query:str -sql query \n
                2.params:tuple (optional) - a tuple of params to set in the sql query.
            this func return:
                1. data:list<tuples> - any tuple in the list is a row in DB
                2.column_names : list
            errors-
             mysql.connector.errors.DatabaseError - this will be rais if db not connected. \n
             mysql.connector.errors.ProgrammingError -this will be rais if db not exists or query is incorrect.\n
        """
        curser = self.__get_cursor()
        try:
            curser.execute(query, params)
            result = curser.fetchall()
            self.__logger.debug(f'The query "{curser.statement}" return {curser.rowcount} rows')
            return result, list(curser.column_names)
        except mysql.connector.errors.ProgrammingError as err:
            self.__logger.error(f'execute "{query}" failed')
            self.__logger.error(traceback.format_exc())
            raise err
        except Exception as err:
            self.__logger.error(f'execute "{query}" failed')
            self.__logger.error(traceback.format_exc())
            raise err

    def query_df(self, sql_query: str, params: tuple = None):
        result, columns = self.query(sql_query, params)
        if not result:
            return None
        df = pandas.DataFrame(data=result, columns=columns)
        return df
