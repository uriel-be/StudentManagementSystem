# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from mysql_connection import Mysql_connection
from logger import  build_logger
import os

# Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    build_logger('./logs/')
    con = Mysql_connection('localhost', 3306)
    con.login('user1', 'User1')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
