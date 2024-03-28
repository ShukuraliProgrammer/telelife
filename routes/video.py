import shutil

import fastapi
import pydantic
import typing
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from functions.video import get_video, add_uservideo, update_uservideo, delete_uservideo, create_videolike
from db import get_db
from models.files import Files
from models.video import Video, VideoLike
from routes.auth import get_current_active_user
from schemas.Users_name import UserCurrent
from schemas.video import videoUpdate, videoCreate, VideoAddLikeRequest


video_router = APIRouter()

app = fastapi.FastAPI()


class Response(pydantic.BaseModel):
    yo: str



@video_router.get("", status_code=200)
async def get_all_users(search: str = None, status: bool = True, roll: str = None, page: int = 1, limit: int = 25,
                db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):
    return get_video(search=search, status=status, roll=roll, page=page, limit=limit,db=db)



@video_router.post("/add")
async def user_add(name:str,
                   janr: str,


                   files: typing.Optional[list[UploadFile]] = File (None),
        db: Session = Depends(get_db),current_user: UserCurrent = Depends(
            get_current_active_user)):
    new_uservideo = Video(

        user_id=current_user.id,
        name=name,
        janr=janr,

    )
    db.add(new_uservideo)
    db.commit()

    if files:
        for file in files:
            with open("media/" + file.filename, 'wb') as image:
                shutil.copyfileobj(file.file, image)
            url = str('media/' + file.filename)
            new_files = Files(
                name=file.filename,
                source_id=new_uservideo.id,
                source="user",
                url=url,
                user_id=current_user.id
            )
            db.add(new_files)
            db.commit()

    raise HTTPException(status_code=200, detail="Amaliyot muvoffaqiyatli amalga oshirildi")


import json
@video_router.post("/add_like")
async def add_like_to_video(data: VideoAddLikeRequest, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):
    try:
        new_likervideo = create_videolike(data.video_id, current_user, db)
        if new_likervideo is None:
            raise HTTPException(status_code=400, detail="Bunday video mavjud")
        return {
            'msg':'Muvoffaqiyatli qo\'shildi', 
            'data': new_likervideo
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Xatolik yuz berdi")
    

@video_router.put("/update")
async def user_update(id: str,
                   name:str,

                   janr:str,
                   files: typing.Optional[list[UploadFile]] = File (None),
        db: Session = Depends(get_db),current_user: UserCurrent = Depends(
            get_current_active_user)):
    new_uservideo=db.query(Video).filter(Video.id == id).update({
        Video.id: id,
        Video.user_id: current_user.id,
        Video.name: name,
        Video.janr: janr

    })
    db.commit()

    if files:
        for file in files:
            with open("media/" + file.filename, 'wb') as image:
                shutil.copyfileobj(file.file, image)
            url = str('media/' + file.filename)
            new_files = Files(
                name=file.filename,
                source_id=id,
                source="user",
                url=url,
                user_id=current_user.id
            )
            db.add(new_files)
            db.commit()
    raise HTTPException(status_code=200, detail="Amaliyot muvoffaqiyatli amalga oshirildi")


@video_router.delete("/delete")
async def user_delete(id: int, db: Session = Depends(get_db),current_user: UserCurrent = Depends(
            get_current_active_user)):
    return delete_uservideo(id=id, user=current_user,db=db)

