from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, ValidationError, validator
from sqlalchemy.orm import Session


class BugBase(BaseModel):
    title: str = Field(..., min_length=5)
    description: str = Field(..., min_length=20)
    status: str = Field(default="open")
    createdBy: str = Field(...)
    createdAt: str = Field(None)
    assignedTo: str = Field(None)

    def __init__(self, title: str, description: str, createdBy: str):
        super().__init__(title=title, description=description, createdBy=createdBy)
        self.createdAt = datetime.now().isoformat()


class Bug(BugBase):
    uuid: str = Field(None)

    def __init__(self, title: str, description: str, createdBy: str):
        super().__init__(title=title, description=description, createdBy=createdBy)
        self.uuid = self.set_id()

    def set_id(self):
        return str(uuid4())
