import logging
from typing import List

import jinja2
import pandas as pd
from pydantic import BaseModel

from src.database.DBFunctions import (check_table_exists, create_table,
                                      execute_query, insert_df_to_table,
                                      query_to_df)
from src.database.models.bugs import Bug
from src.database.routes.UserDBFunctions import (USER_TABLENAME,
                                                 check_user_exists)

BUG_TABLENAME = "bugs"


class SimpleBug(BaseModel):
    uuid: str
    title: str
    status: str


class ListBug(BaseModel):
    bugs: List[SimpleBug]


def create_bug_table(sqlite_db_path: str, table: str = BUG_TABLENAME):
    create_table(
        sqlite_db_path,
        table,
        [
            "uuid VARCHAR(225) PRIMARY KEY",
            "title VARCHAR(255) NOT NULL",
            "description VARCHAR(255) NOT NULL",
            "status VARCHAR(255) NOT NULL",
            "createdBy VARCHAR(255)",
            "createdAt VARCHAR(255)",
            "assignedTo VARCHAR(255)",
        ],
    )
    return sqlite_db_path, table


def create_bug(sqlite_db_path: str, bug: Bug, table: str = BUG_TABLENAME) -> None:
    if not check_table_exists(sqlite_db_path, table):
        logging.info(f"Table {table} does not exists, create {table} table")
        create_bug_table(sqlite_db_path, table)
    df = pd.DataFrame.from_dict({k: [v] for k, v in bug.dict().items()})
    logging.info(bug.dict())
    try:
        insert_df_to_table(sqlite_db_path, table, df)
    except Exception as e:
        raise e


def list_bug(
    sqlite_db_path: str, status: str, table: str = BUG_TABLENAME
) -> pd.DataFrame:
    if not check_table_exists(sqlite_db_path, table):
        create_bug_table(sqlite_db_path, table)

    status_options = ["open", "close", "any"]
    if status.lower() not in status_options:
        raise ValueError(f"Invalid status option {status}")
    query_param = dict(table=table, status=status)
    query = """SELECT uuid, title, status FROM {{table}} WHERE 
    {% if status in ['open', 'any']%} status = 'open' {% if status == 'any'%} OR {%endif%}{%endif%}
    {% if status in ['close', 'any']%} status = 'close' {%endif%}"""
    list_bug_query = jinja2.Environment().from_string(query).render(**query_param)
    return query_to_df(sqlite_db_path, list_bug_query)


def check_bug_exists(
    sqlite_db_path: str, bug_id: str, table: str = BUG_TABLENAME
) -> bool:
    query_param = dict(table=table, bug_id=bug_id)
    query = """SELECT uuid, title FROM {{table}} WHERE uuid = '{{bug_id}}'"""
    check_bug_query = jinja2.Environment().from_string(query).render(**query_param)
    check_bug_results = execute_query(sqlite_db_path, check_bug_query)
    if check_bug_results:
        return True
    return False


def assign_bug(
    sqlite_db_path: str,
    bug_id: str,
    user_id: str,
    bug_table: str = BUG_TABLENAME,
    user_table: str = USER_TABLENAME,
):
    if not check_table_exists(sqlite_db_path, bug_table):
        create_bug_table(sqlite_db_path, bug_table)

    if not check_bug_exists(sqlite_db_path, bug_id, bug_table):
        raise ValueError(f"Bug id {bug_id} does not exists")

    if not check_user_exists(sqlite_db_path, {"uuid": user_id}, user_table):
        raise ValueError(f"User id {user_id} does not exists")

    query_param = dict(bug_id=bug_id, user_id=user_id, table=bug_table)
    query = (
        """UPDATE {{table}} SET assignedTo = '{{user_id}}' WHERE uuid = '{{bug_id}}';"""
    )
    assign_bug_query = jinja2.Environment().from_string(query).render(**query_param)
    execute_query(sqlite_db_path, assign_bug_query)
    return query_to_df(
        sqlite_db_path,
        f"""SELECT 
        uuid,
        title, 
        description, 
        status, 
        createdBy, 
        createdAt, 
        assignedTo 
        FROM {bug_table} 
        WHERE uuid = '{bug_id}';""",
    ).to_dict("records")[0]


def close_bug(sqlite_db_path: str, bug_id: str, bug_table: str = BUG_TABLENAME):
    if not check_table_exists(sqlite_db_path, bug_table):
        create_bug_table(sqlite_db_path, bug_table)

    if not check_bug_exists(sqlite_db_path, bug_id, bug_table):
        raise ValueError(f"Bug id {bug_id} does not exists")

    query_param = dict(bug_id=bug_id, table=bug_table)
    query = """UPDATE {{table}} SET status = 'close' WHERE uuid = '{{bug_id}}'"""
    close_bug_query = jinja2.Environment().from_string(query).render(**query_param)
    execute_query(sqlite_db_path, close_bug_query)
    return query_to_df(
        sqlite_db_path,
        f"""SELECT 
            title, 
            description, 
            status, 
            createdBy, 
            createdAt, 
            assignedTo,
            uuid
            FROM {bug_table} 
            WHERE uuid = '{bug_id}';""",
    ).to_dict("records")[0]


def get_bug(sqlite_db_path: str, bug_id: str, table: str = BUG_TABLENAME):
    if not check_table_exists(sqlite_db_path, table):
        create_bug_table(sqlite_db_path, table)

    if not check_bug_exists(sqlite_db_path, bug_id, table):
        raise ValueError(f"Bug id {bug_id} does not exists")

    return query_to_df(
        sqlite_db_path,
        f"""SELECT 
                uuid,
                title, 
                description, 
                status, 
                createdBy, 
                createdAt, 
                assignedTo 
                FROM {table} 
                WHERE uuid = '{bug_id}';""",
    ).to_dict("records")[0]
