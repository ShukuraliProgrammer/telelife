from pydantic import BaseModel


class followersBase(BaseModel):
    follower_id: str
    user_id: str


class followersCreate(followersBase):
    pass


class followersUpdate(followersBase):
    id: int


