import logging
import sqlite3

import jinja2
import pandas as pd

USER_TABLENAME = "users"
# BUG_TABLE = "bugs"
# BUG_UPDATE_TABLE = "bug_updates"


def get_connection(sqlite_server="bug_tracker.db"):
    return sqlite3.connect(sqlite_server)


def get_cursor(connection: sqlite3.Connection):
    return connection.cursor()


def execute_query(sqlite_db_path: str, query: str):
    logging.debug(f"Execute query to db '{sqlite_db_path}': \n{query}")
    print(query)
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
    query = f"""SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='{table}'; """
    listOfTables = execute_query(sqlite_db_path=sqlite_db_path, query=query)
    if not listOfTables:
        return False
    return True
