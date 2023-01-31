from fastapi import FastAPI
from pydantic_sqlite import DataBase
from pydantic import ValidationError
from src.database.models.users import User, UserBase
from src.database.models.bugs import Bug
from src.database.routes.UserDBFunctions import get_user, update_user, create_user
from src.database.routes.BugDBFunctions import list_bug, create_bug, assign_bug, close_bug, get_bug

from logging.config import dictConfig
import logging
from config import LogConfig
from config import DATABASE_SOURCE

dictConfig(LogConfig().dict())
logger = logging.getLogger("bug_tracker_api")

app = FastAPI()
db = DataBase()


@app.post("/user/")
async def create_user_(user: User):
    """
    api end point to create users
    :param user:
    :return:
    """
    try:
        create_user(DATABASE_SOURCE, user)
        return {"user": user.dict(), "status": 200}
    except ValidationError as e:
        logger.error(e)
        return {"error": repr(e), "status": 400}


@app.get("/user/{username}")
async def get_user_(username: str):
    """

    :param username:
    :return:
    """
    df = get_user(DATABASE_SOURCE, dict(username=username))
    return {'user': df.to_dict('records')}


@app.post("/user/update/")
async def update_username(username: str, user: UserBase):
    """

    :param username:
    :param user:
    :return:
    """
    user_results = get_user(DATABASE_SOURCE, dict(user.dict())).to_dict('records')
    if len(user_results) > 1:
        raise Exception(f'More than one user match error, \n user params: {user.dict()}')
    target_user = user_results[0]
    target_user_id = target_user.get("uuid")
    update_user(DATABASE_SOURCE, user_login=user.dict(), change=dict(username=username))
    new_user_dict = get_user(DATABASE_SOURCE, dict(uuid=target_user_id)).to_dict('records')[0]
    return {"userid": target_user_id, "update": new_user_dict}


@app.get("/bug/list/")
async def list_bug_by_status(status: str = 'any'):
    bug_df = list_bug(DATABASE_SOURCE, status)
    return {"bugs": bug_df.to_dict('records')}

@app.get("/bug/")
async def get_bug_(bugid:str):
    return {"bug":get_bug(DATABASE_SOURCE, bugid)}


@app.post("/bug/")
async def create_bug_(bug: Bug):
    try:
        create_bug(DATABASE_SOURCE, bug)
        return {"status": "success", "bug": bug.dict()}
    except ValidationError as e:
        return {"status": "failed", "error": repr(e)}

@app.post('/bug/assign/')
async def assign_bug_(userid: str, bugid:str):
    try:
        bug_new_status = assign_bug(DATABASE_SOURCE, bugid, userid)
        return {"status": "success", "bug": bug_new_status}
    except Exception as e:
        return {"status": "failed", "error": repr(e)}


@app.post('/bug/close/')
async def close_bug_(bugid:str):
    try:
        bug_new_status = close_bug(DATABASE_SOURCE, bugid)
        return {"status": "success", "bug": bug_new_status}
    except Exception as e:
        return {"status": "failed", "error": repr(e)}
