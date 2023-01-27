from fastapi import FastAPI
from pydantic_sqlite import DataBase
from pydantic import ValidationError
from src.database.models.users import User, User_details
from src.database.models.bugs import Bug
from src.database.models.bug_updates import Bug_updates
from uuid import uuid4
import logging
from logging.config import dictConfig
import logging
from config import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("mycoolapp")

app = FastAPI()
db = DataBase()


@app.post("/user/")
async def create_user(user: User_details):
    try:
        user_param = {"uuid": str(uuid4())}
        user_param.update(user.dict())
        u = User(**user_param)
        db.add("user", u)
        db.save("hello_world.db")
        return {"user": u.dict(), "status": 200}
    except ValidationError as e:
        logger.error(e)
        return {"error": repr(e), "status": 400}


@app.get("/user/{userid}")
async def get_user(userid: str):
    return {"userid": userid}


@app.post("/bug/")
async def create_bug(bug: Bug):
    bug.create()


@app.post("/bug/{bug_id}/update")
async def create_bug_update(bug_id: str, bug_update: Bug_updates):
    pass