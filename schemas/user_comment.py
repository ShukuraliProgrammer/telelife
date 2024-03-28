from pydantic import BaseModel
from typing import Optional, List


class commentBase(BaseModel):
    video_id: int
    user_id: int


class commentCreate(commentBase):
    pass


class commentUpdate(commentBase):
    id: int


