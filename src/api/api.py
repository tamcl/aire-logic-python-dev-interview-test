import logging
from logging.config import dictConfig
from typing import List

from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from pydantic_sqlite import DataBase

from config import DATABASE_SOURCE, LogConfig
from src.database.models.bugs import Bug
from src.database.models.users import User, UserBase
from src.database.routes.BugDBFunctions import (ListBug, assign_bug, close_bug,
                                                create_bug, get_bug, list_bug)
from src.database.routes.UserDBFunctions import (create_user, get_user,
                                                 update_user)

dictConfig(LogConfig().dict())
logger = logging.getLogger("bug_tracker_api")

tags_metadata = [
    {"name": "users", "description": "Operations with users"},
    {"name": "bugs", "description": "Operations with bugs"},
]

app = FastAPI()
db = DataBase()


@app.post("/user/", tags=["users"], response_model=User)
async def create_user_(
    user: User = Body(example={"username": "jakesmith", "email": "jake@example.com"})
):
    """
    Create User

    """
    try:
        create_user(DATABASE_SOURCE, user)
        return JSONResponse(status_code=200, content=user.dict())
    except ValidationError as e:
        logger.error(e)
        return {"error": repr(e), "status": 400}


@app.get("/user/{username}", tags=["users"], response_model=User)
async def get_user_(username: str):
    """
        Retrieve user details
    """
    df = get_user(DATABASE_SOURCE, dict(username=username))
    return JSONResponse(status_code=200, content=df.to_dict("records")[0])


@app.post("/user/update/", tags=["users"], response_model=User)
async def update_username(newUsername: str, user: UserBase):
    """
        Update user username
    """
    # TODO need to check the username validation
    user_results = get_user(DATABASE_SOURCE, dict(user.dict())).to_dict("records")
    if len(user_results) > 1:
        raise Exception(
            f"More than one user match error, \n user params: {user.dict()}"
        )
    target_user = user_results[0]
    target_user_id = target_user.get("uuid")
    update_user(
        DATABASE_SOURCE, user_login=user.dict(), change=dict(username=newUsername)
    )
    new_user_dict = get_user(DATABASE_SOURCE, dict(uuid=target_user_id)).to_dict(
        "records"
    )[0]
    return JSONResponse(status_code=200, content=new_user_dict)


@app.get("/bug/list/", tags=["bugs"], response_model=ListBug)
async def list_bug_by_status(status: str = "any"):
    """
    List all bugs (simplified details) with different status
    [open, close, any]

    """
    if status not in ["open", "close", "any"]:
        return JSONResponse(status_code=400, content={"error": "Unknown status"})
    bug_df = list_bug(DATABASE_SOURCE, status)
    return JSONResponse(status_code=200, content={"bugs": bug_df.to_dict("records")})


@app.get("/bug/", tags=["bugs"], response_model=Bug)
async def get_bug_(bugid: str):
    """
    Retrieve single bug details

    """
    return JSONResponse(status_code=200, content=get_bug(DATABASE_SOURCE, bugid))


@app.post("/bug/", tags=["bugs"], response_model=Bug)
async def create_bug_(
    bug: Bug = Body(
        example=dict(
            title="Place Bug title here",
            description="This will a description of what the bug is",
            createdBy="69f37564-fc57-4d81-a71f-5b04ceb6942e",
        )
    )
):
    """
    create a bug

    """
    try:
        create_bug(DATABASE_SOURCE, bug)
        return JSONResponse(status_code=200, content=bug.dict())
    except ValidationError as e:
        return JSONResponse(status_code=400, content={repr(e)})


@app.post("/bug/assign/", tags=["bugs"], response_model=Bug)
async def assign_bug_(userid: str, bugid: str):
    """
    assign bug to a user

    """
    try:
        bug_new_status = assign_bug(DATABASE_SOURCE, bugid, userid)
        return JSONResponse(status_code=200, content=bug_new_status)
    except Exception as e:
        return JSONResponse(content={"error": repr(e)})


@app.post("/bug/close/", tags=["bugs"], response_model=Bug)
async def close_bug_(bugid: str):
    """
    close a bug

    """
    try:
        bug_new_status = close_bug(DATABASE_SOURCE, bugid)
        return JSONResponse(status_code=200, content=bug_new_status)
    except Exception as e:
        return {"status": "failed", "error": repr(e)}
