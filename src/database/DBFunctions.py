# import sqlite3
# from sqlalchemy import create_engine, ForeignKey
# from sqlalchemy import Column, Date, Integer, String
# from sqlalchemy.ext.declarative import declarative_base


# Base = declarative_base()

# conn = sqlite3.connect("database.db")


# class SQLiteDBSetup:
#     def __init__(self, db_source="database.db"):
#         self.db_source = db_source
#         self.conn = None
#
#     def connect(self):
#         self.conn = sqlite3.connect(self.db_source)
#
#     def close(self):
#         self.conn
# def get_engine():
#     return create_engine()

from pydantic_sqlite import DataBase
from src.database.models import *

def get_db():
    return DataBase()

def check_user_detail_with_username(username:str, db: DataBase, table:str = ""):
    for i in db("user"):
        print(i)
        if i.dict().get('username') == username:
            return True
    return False
