import shutil
import typing
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from functions.user_comment import get_comment, add_usercomment, update_usercomment, delete_usercomment
from db import get_db
from models.files import Files
from routes.auth import get_current_active_user
from schemas.Users_name import UserCurrent
from schemas.user_comment import commentUpdate, commentCreate
from models.user_comment import Users_comment

comment_router = APIRouter()


@comment_router.get("", status_code=200)
async def get_all_users(search: str = None, status: bool = True,  roll: str = None, page: int = 1,
                        limit: int = 25,
                        db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):
    return get_comment(search=search, status=status, roll=roll, page=page, limit=limit, db=db)


@comment_router.post("/add")
async def user_add(video_id:int,
                   files: typing.Optional[list[UploadFile]] = File (None),
                    db: Session = Depends(get_db),current_user: UserCurrent = Depends(
            get_current_active_user)):

    new_user_comment = Users_comment(
        user_id=current_user.id,
        video_id=video_id,

    )
    db.add(new_user_comment)
    db.commit()

    if files:
        for file in files:
            with open("media/" + file.filename, 'wb') as image:
                shutil.copyfileobj(file.file, image)
            url = str('media/' + file.filename)
            new_filese = Files(
                name=file.filename,
                source_id=new_user_comment.id,
                source="user",
                url=url,
                user_id=current_user.id


            )
            db.add(new_filese)
            db.commit()



    raise HTTPException(status_code=200, detail="Amailiyot muvoffaqiyatli amalga oshirli")


@comment_router.put("/update")
async def user_update(id: int,
                   video_id:int,

                   files: typing.Optional[list[UploadFile]] = File (None),
        db: Session = Depends(get_db),current_user: UserCurrent = Depends(
            get_current_active_user)):
    new_user_comment=db.query(Users_comment).filter(Users_comment.id == id).update({
        Users_comment.id: id,
        Users_comment.user_id: current_user.id,
        Users_comment.video_id: video_id,
    }
    )
    db.commit()

    if files:
        for file in files:
            with open("media/" + file.filename, 'wb') as image:
                shutil.copyfileobj(file.file, image)
            url = str('media/' + file.filename)
            new_filese = Files(
                name=file.filename,
                source_id=id,
                source="user",
                url=url,
                user_id=current_user.id


            )
            db.add(new_filese)
            db.commit()

    raise HTTPException(status_code=200, detail="Amailiyot muvoffaqiyatli amalga oshirli")


@comment_router.delete("/delete")
async def user_delete(id: int, db: Session = Depends(get_db),current_user: UserCurrent = Depends(
            get_current_active_user)):
    return delete_usercomment(id=id, user=current_user,db=db)

