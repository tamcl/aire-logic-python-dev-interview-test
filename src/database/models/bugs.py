from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from pydantic import validator, ValidationError, Field




class Bug(BaseModel):
    id: str = Field(None)
    title: str = Field(...,min_length=5)
    description: str = Field(..., min_length=10)
    createdBy: str = Field
    createdAt: str

    # @validator('title')
    # def check_title(cls, v):


    def create(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
