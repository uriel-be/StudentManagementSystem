import mysql.connector as connector
import mysql.connector.errors
import logging


class Mysql_connection:
    def __init__(self, hostname, port=3306):
        self.__is_connected = False
        self.__connection = None
        self.__logger = logging.getLogger("logger")
        self.hostname = hostname
        self.port = port

    def is_connected(self):
        return self.__is_connected

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




