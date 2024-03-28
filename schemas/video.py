from pydantic import BaseModel


class videoBase(BaseModel):
    name: str
    user_id: str
    janr: str
    like_number:int



class videoCreate(videoBase):
    pass


class videoUpdate(videoBase):
    id: int

class VideoAddLikeRequest(BaseModel):
    video_id: int