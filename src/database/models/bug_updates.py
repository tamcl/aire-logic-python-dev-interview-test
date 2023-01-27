from pydantic import BaseModel
from pydantic import validator, ValidationError, Field
import hashlib


def get_bug_update_id(param: dict):
    keys = list(param.keys())
    keys.sort()
    hash_id = hashlib.md5(''.join([str(param.get(i)) for i in keys]).encode('utf-8'))
    return hash_id.hexdigest()


class Bug_updates_details(BaseModel):
    update: str = Field(None, description="additional comments on the bug")
    status: str = Field(None, description="status change on the bug tracking")
    updatedAt: str = Field(..., description="user that updates the bug details")
    updatedBy: str = Field(..., description="the time for the bug gets the update")

    @validator('status')
    def status_update_check(cls, v):
        """
        Only allow status to either be 'Open', 'Processing', or 'Closed'
        :param v:
        :return:
        """
        status_code = ['Open', 'Processing', 'Closed']
        if v not in status_code:
            raise ValueError(f'invalid status. status can only be {status_code}')
        return v

    @validator('updatedBy')
    def updatedBy_time_check(cls, v):
        return v

    def create_update(self, bug_id: str):
        update_param = {
            "bug_id"       : bug_id,
            "bug_update_id": get_bug_update_id(self.dict())
        }
        update_param.update(self.dict())
        Bug_updates(**update_param)


class Bug_updates(Bug_updates_details):
    bug_id: str = Field(..., description="")
    bug_update_id: str
