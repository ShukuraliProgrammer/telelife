import shutil
import typing
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from functions.followers import get_folowers, add_userfollowers, update_userfollowers, delete_userupdate
from db import get_db
from models.files import Files
from models.followers import users_followers
from routes.auth import get_current_active_user
from schemas.Users_name import UserCurrent

from schemas.followers import followersUpdate, followersCreate

followers_router = APIRouter()


@followers_router.get("", status_code=200)
async def get_all_users(search: str = None, status: bool = True,roll: str = None, page: int = 1, limit: int = 25,
                db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):
    return get_folowers(search=search, status=status, roll=roll, page=page, limit=limit,db=db)


@followers_router.post("/add")
async def user_add(follower_id:str,

                   files: typing.Optional[list[UploadFile]] = File (None),
                    db: Session = Depends(get_db),current_user: UserCurrent = Depends(
            get_current_active_user)):

    new_userfollowers = users_followers(
        user_id=current_user.id,
        follower_id=follower_id,
    )
    db.add(new_userfollowers)
    db.commit()

    if files:
        for file in files:
            with open("media/" + file.filename, 'wb') as image:
                shutil.copyfileobj(file.file, image)
            url = str('media/' + file.filename)
            new_fileses = Files(
                name=file.filename,
                source_id=new_userfollowers.id,
                source="user",
                url=url,
                user_id=current_user.id
            )
            db.add(new_fileses)
            db.commit()

    raise HTTPException(status_code=200, detail="Amaliyot muvoffaqiyatli amalga oshirildi")



@followers_router.put("/update")
async def user_update(id: str,
                      follower_id:str,

                      files: typing.Optional[list[UploadFile]] = File (None),

                      db: Session = Depends(get_db),current_user: UserCurrent = Depends(
            get_current_active_user)):
    new_userfollowers=db.query(users_followers).filter(users_followers.id == id).update({
        users_followers.id: id,
        users_followers.user_id: current_user.id,
        users_followers.follower_id: follower_id,

    })
    db.commit()

    if files:
        for file in files:
            with open("media/" + file.filename, 'wb') as image:
                shutil.copyfileobj(file.file, image)
            url = str('media/' + file.filename)
            new_fileses = Files(
                name=file.filename,
                source_id=id,
                source="user",
                url=url,
                user_id=current_user.id
            )
            db.add(new_fileses)
            db.commit()

    raise HTTPException(status_code=200, detail="Amaliyot muvoffaqiyatli amalga oshirildi")


@followers_router.delete("/delete")
async def user_delete(id: int, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):
    return delete_userupdate(id=id,user=current_user, db=db)


