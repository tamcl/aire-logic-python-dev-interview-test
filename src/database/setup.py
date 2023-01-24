import sqlite3

conn = sqlite3.connect('database.db')

class SQLiteDBSetup:
    def __init__(self, db_source = 'database.db'):
        self.db_source = db_source
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_source)

    def close(self):
        self.conn