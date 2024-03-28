from pydantic import BaseModel
from typing import Optional, List


# 1 chsiga

class UserBase(BaseModel):
    name: str
    username: str
    roll: str
    password: str
    number: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    id: int


class Token(BaseModel):
    access_token = str
    token = str


class TokenData(BaseModel):
    id: int


class UserCurrent(UserBase):
    id: int
    last_name: str
    status: bool
    user_status: bool
    bio: str
    phone: str
    create_at: str


