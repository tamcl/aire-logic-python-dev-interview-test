# import sqlite3
# from sqlalchemy import create_engine, ForeignKey
# from sqlalchemy import Column, Date, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
from pydantic_sqlite import DataBase
from src.database.models import *

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

def get_db():
    return DataBase()