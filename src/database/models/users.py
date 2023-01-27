from pydantic import BaseModel
from pydantic import validator, ValidationError
import re
from uuid import uuid4
import logging


class User_details(BaseModel):
    username: str
    email: str
    password: str # normally password should be hashed for security reasons

    @validator('email')
    def check_email(cls, v):
        email_validator = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
        if re.fullmatch(email_validator, v):
            return v
        else:
            raise ValueError("incorrect email format")

    @validator('username')
    def check_username(cls,v):
        return v

    @validator('password')
    def check_password(cls, v):
        if re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$", v):
            return v
        else:
            raise ValidationError('Password requirement Minimum eight and maximum 20 characters,'
                                  ' at least one uppercase letter, one lowercase letter, one number'
                                  ' and one special character')

    def create(self):
        pass

    def update_username(self):
        pass

    def update_password(self):
        pass

    def delete_user(self):
        pass

class User(User_details):
    uuid:str
