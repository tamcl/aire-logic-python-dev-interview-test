import logging
import sqlite3
from datetime import datetime

import pandas as pd

from src.database.DBFunctions import (check_table_exists,
                                      create_table, execute_query,
                                      insert_df_to_table,  query_to_df)
from src.database.routes.UserDBFunctions import check_user_exists, get_user, update_user, validate_user, create_user
from src.test.user_test import user_test
from src.test.bug_test import bug_test

# from src.database.models.users import User, USER_TABLE

logging.basicConfig(
    format="%(levelname)s: %(asctime)s - %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S",
)
user_test()
logging.info(query_to_df('bug_tracker.db','SELECT * from users').to_dict('records'))
userid_list = list(query_to_df('bug_tracker.db','SELECT uuid from users').to_dict('series').get('uuid'))
bug_test(*userid_list)
logging.info(query_to_df('bug_tracker.db','SELECT * from bugs').to_dict('records'))
#==================
# if not check_table_exists('bug_tracker.db', 'user'):
#     create_table('bug_tracker.db', 'user', [
#         'uuid VARCHAR(225) PRIMARY KEY',
#         'username VARCHAR(255) UNIQUE',
#         'email VARCHAR(255) UNIQUE',
#         'password VARCHAR(255)'
#     ])
# query = """"""
#==================
# user4 = dict(
#     username="hello4",
#     email="hello4@example.com",
#     password="Pass@123")
# u = User(**user4)
# u.create_user()
# logging.info(check_user_exists('bug_tracker.db', match=dict(username='hello4'), table='user'))
# update_user('bug_tracker.db', match=dict(username='hello4'), change=dict(username='lol'), table='user')
# logging.info(get_user('bug_tracker.db', match=dict(username = 'lol'), table='user'))
#
# logging.info(validate_user('bug_tracker.db', match=dict(email="hello4@example.com", password="Pass@123"), table='user'))
#
# def test_function(*param):
#     print(param)
#
# USER_TABLE_PARAM = ['user', 'something'] + USER_TABLE
# test_function(*USER_TABLE_PARAM)

