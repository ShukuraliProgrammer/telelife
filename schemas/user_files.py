from pydantic import BaseModel
from typing import Optional, List


class filesBase(BaseModel):
    name: str
    user_id: str


class filesCreate(filesBase):
    pass


class filesUpdate(filesBase):
    id: int

