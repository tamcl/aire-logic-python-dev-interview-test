import sqlite3
import logging

logging.basicConfig(
    format="%(levelname)s: %(asctime)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute(
    """CREATE TABLE tasks 
                  (id INTEGER PRIMARY KEY, title TEXT, description TEXT)"""
)
conn.commit()
conn.close()
