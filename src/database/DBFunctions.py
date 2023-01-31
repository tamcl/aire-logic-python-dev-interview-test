import logging
import sqlite3

import jinja2
import pandas as pd
from config import DATABASE_SOURCE


def get_connection(sqlite_server=DATABASE_SOURCE):
    """
    create or connect to sqlite database server
    :param sqlite_server:
    :return:
    """
    return sqlite3.connect(sqlite_server)


def get_cursor(connection: sqlite3.Connection):
    """
    create cursor from the sqlite server connection
    :param connection:
    :return:
    """
    return connection.cursor()


def execute_query(sqlite_db_path: str, query: str):
    """
    function that can execute an SQL query
    :param sqlite_db_path:
    :param query:
    :return:
    """
    logging.debug(f"Execute query to db '{sqlite_db_path}': \n{query}")
    if sqlite_db_path:
        conn = get_connection(sqlite_db_path)
    else:
        conn = get_connection()
    cursor = get_cursor(conn)
    try:
        query_results = cursor.execute(query).fetchall()
    except Exception as e:
        raise e
    finally:
        conn.commit()
        conn.close()
    return query_results


def insert_df_to_table(
    sqlite_db_path: str, table: str, df: pd.DataFrame, if_exists="append"
):
    """
    function that can insert rows of data into a sqlite server table
    :param sqlite_db_path:
    :param table:
    :param df:
    :param if_exists:
    """
    if sqlite_db_path:
        conn = get_connection(sqlite_db_path)
    else:
        conn = get_connection()
    try:
        df.to_sql(table, conn, if_exists=if_exists, index=False)
    finally:
        conn.commit()
        conn.close()


def query_to_df(sqlite_db_path: str, query: str):
    """
    function that can return a pandas dataframe from a query
    :param sqlite_db_path:
    :param query:
    :return:
    """
    if sqlite_db_path:
        conn = get_connection(sqlite_db_path)
    else:
        conn = get_connection()
    try:
        return pd.read_sql(query, conn)
    finally:
        conn.commit()
        conn.close()


def create_table(sqlite_db_path, table_name: str, column_details: list):
    """
    function that can create a table in the sqlite database server
    :param sqlite_db_path:
    :param table_name:
    :param column_details:
    """
    query_param = dict(table_name=table_name, columns=column_details)
    query = """
    CREATE TABLE {{table_name}}
    (
    {% for i in columns %}{{i}}{% if not loop.last %}, {% endif %}
    {%endfor%}
    );"""

    create_table_query = jinja2.Environment().from_string(query).render(**query_param)
    try:
        execute_query(sqlite_db_path=sqlite_db_path, query=create_table_query)
    except sqlite3.OperationalError as e:
        raise e


def check_table_exists(sqlite_db_path: str, table: str):
    """
    function that can identify if a table exists in sqlite database server
    :param sqlite_db_path:
    :param table:
    :return:
    """
    query = f"""SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='{table}'; """
    listOfTables = execute_query(sqlite_db_path=sqlite_db_path, query=query)
    if not listOfTables:
        return False
    return True
