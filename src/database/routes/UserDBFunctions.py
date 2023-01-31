
import jinja2
import pandas as pd

from src.database.DBFunctions import (check_table_exists, create_table,
                                      execute_query, insert_df_to_table,
                                      query_to_df)
from src.database.models.users import User

USER_TABLENAME = "users"


def create_user_table(sqlite_db_path: str, table: str = USER_TABLENAME):
    """
    function that can create a bug table in desired sqlite database
    :param sqlite_db_path:
    :param table:
    :return:
    """
    create_table(
        sqlite_db_path,
        table,
        [
            "uuid VARCHAR(225) PRIMARY KEY",
            "username VARCHAR(255) UNIQUE",
            "email VARCHAR(255) UNIQUE",
            # 'password VARCHAR(255)'
        ],
    )
    return sqlite_db_path, table


def check_user_exists(sqlite_db_path: str, match: dict, table: str = USER_TABLENAME):
    """
    function that can check if there are user with the matching input detials
    :param sqlite_db_path:
    :param match:
    :param table:
    :return:
    """
    query_param = dict(table=table, match=match)
    query = """SELECT * from {{table}} WHERE 
{% for k, v in match.items()%}{{k}} = '{{v}}' {% if not loop.last %}OR {% endif %}{% endfor %}"""
    find_user_query = jinja2.Environment().from_string(query).render(**query_param)
    ListOfMatch = execute_query(sqlite_db_path=sqlite_db_path, query=find_user_query)
    if ListOfMatch:
        return True
    return False


def create_user(sqlite_db_path: str, user: User, table: str = USER_TABLENAME):
    """
    function that can create a user in the user table in the sqlite database server
    :param sqlite_db_path:
    :param user:
    :param table:
    """
    if not check_table_exists(sqlite_db_path, table):
        create_user_table(sqlite_db_path)
    assert user.uuid is not None
    assert user.username is not None
    assert user.email is not None
    # assert user.password is not None

    match_param = user.dict().copy()
    # del match_param['password']
    del match_param["uuid"]
    if not check_user_exists(
        sqlite_db_path=sqlite_db_path, match=match_param, table=table
    ):
        df = pd.DataFrame.from_dict({k: [v] for k, v in user.dict().items()})
        insert_df_to_table(sqlite_db_path, table, df)
    else:
        raise ValueError("user already exists")


def get_user(
    sqlite_db_path: str, match: dict, table: str = USER_TABLENAME
) -> pd.DataFrame:
    """
    function that can get the user from matching user details
    :param sqlite_db_path:
    :param match:
    :param table:
    :return:
    """
    query_param = dict(table=table, match=match)
    query = """SELECT uuid, username, email from {{table}} WHERE 
    {% for k, v in match.items()%}{{k}} = '{{v}}' {% if not loop.last %}AND {% endif %}{% endfor %}"""
    get_user_query = jinja2.Environment().from_string(query).render(**query_param)
    return query_to_df(sqlite_db_path, get_user_query)


def update_user(
    sqlite_db_path: str, user_login: dict, change: dict, table: str = USER_TABLENAME
):
    """
    function that can update user details by finding the user that has the matching details
    :param sqlite_db_path:
    :param user_login:
    :param change:
    :param table:
    """
    # TODO only change username, need to check other username exists
    # TODO cannot change uuid
    query_param = dict(table=table, match=user_login, change=change)
    query = """UPDATE {{table}} 
    SET {% for k,v in change.items() %} {{k}} = '{{v}}' {% if not loop.last %}, {% endif %} {% endfor %} 
    WHERE {% for k,v in match.items() %} {{k}} = '{{v}}' {% if not loop.last %}AND {% endif %} {% endfor %} """
    update_user_query = jinja2.Environment().from_string(query).render(**query_param)
    execute_query(sqlite_db_path, update_user_query)


def validate_user(
    sqlite_db_path: str, match: dict, table: str = USER_TABLENAME
) -> bool:
    """
    Validating the login of the user, due to time contraints, I am not able to implement a full login system
    but some implementation is here

    :param sqlite_db_path:
    :param match:
    :param table:
    :return:
    """
    match_param = dict()
    if match.get("username") is None and match.get("email") is None:
        raise ValueError("username or email not provided")

    if match.get("username"):
        match_param.update(dict(username=match.get("username")))

    if match.get("email"):
        match_param.update(dict(email=match.get("email")))

    if not check_user_exists(sqlite_db_path, match=match_param, table=table):
        raise ValueError("user does not exist")

    if match.get("password") is None:
        raise ValueError("password not given")
    else:
        match_param.update(dict(password=match.get("password")))

    query = """SELECT uuid FROM {{table}}
    WHERE {% if match_param.get('username') %} username = '{{match_param.get('username')}}' AND {% endif -%}
    {% if match_param.get('email') %} email = '{{match_param.get('email')}}' AND {% endif %}
    password = '{{match_param.get('password')}}'"""
    validate_user_query = (
        jinja2.Environment()
        .from_string(query)
        .render(table=table, match_param=match_param)
    )
    validation_results = execute_query(sqlite_db_path, validate_user_query)
    if validation_results is None:
        return False
    return True
