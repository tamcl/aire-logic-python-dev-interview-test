import logging
import re
from typing import Optional
from uuid import uuid4

import jinja2
import pandas as pd
from pydantic import BaseModel, Field, PrivateAttr, ValidationError, validator
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# from src.database.routes.UserDBFunctions import check_user_exists, get_user
from config import DATABASE_SOURCE
from src.database.DBFunctions import check_table_exists, insert_df_to_table

USER_TABLENAME = "user"


class UserBase(BaseModel):
    username: Optional[str] = Field(example="exampleUsername")
    email: Optional[str] = Field(
        None,
        regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        example="example@example.com",
    )

    # password: Optional[str]  # normally password should be hashed for security reasons
    #
    # @validator('password')
    # def check_password(cls, v):
    #     if re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$", v):
    #         return v
    #     else:
    #         raise ValidationError('Password requirement Minimum eight and maximum 20 characters,'
    #                               ' at least one uppercase letter, one lowercase letter, one number'
    #                               ' and one special character')


class User(UserBase):
    uuid: str = Field(None)

    def __init__(self, username: str = None, email: str = None, password: str = None):
        super().__init__(username=username, email=email, password=password)
        self.uuid = self.set_id()

    def set_id(self):
        if self.username is None and self.email is None:
            raise ValueError("username and email is missing")
        if self.username is None:
            pass

        if self.email is None:
            pass

        return str(uuid4())
