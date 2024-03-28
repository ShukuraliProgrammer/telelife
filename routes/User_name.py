import shutil

import fastapi
import pydantic
import typing


from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from functions.User_name import get_users, add_username, update_username, delete_username
from db import get_db
from models.files import Files
from routes.auth import get_current_active_user, get_password_hash
from schemas.Users_name import UserCreate, UserUpdate, UserCurrent
from models.User_name import Users

user_router = APIRouter()


@user_router.get("", status_code=200)
async def get_all_users(search: str = None, status: bool = True, roll: str = None, page: int = 1, limit: int = 25,
                db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):
    return get_users(search=search, status=status, roll=roll, page=page, limit=limit,db=db)


@user_router.post("/QOSHISH")
async def user_add(name:str,
                   user_name:str,
                   roll:str,
                   password:str,
                   phone: str,

                   files:typing.Optional[typing.List[UploadFile]] = File( None)

        , db: Session = Depends(get_db),):
    new_users = Users(
        name=name,
        user_name=user_name,
        roll=roll,
        phone=phone,

        password=get_password_hash(password),

    )
    db.add(new_users)
    db.commit()

    if files:
        for file in files:
            with open("media/" + file.filename, 'wb') as image:
                shutil.copyfileobj(file.file, image)
            url = str('media/' + file.filename)
            new_file = Files(
                name=file.filename,
                source_id=new_users.id,
                source="user",
                url=url,
                user_id=new_users.id

            )
            db.add(new_file)
            db.commit()



            raise HTTPException(status_code=200, detail="Amaliyot muvoffaqiyatli amalga oshirildi")


@user_router.put("/YANGILASH")
async def user_update(id: int,
                   name:str,
                   user_name:str,
                   roll:str,
                   password:str,
                   phone: str,
                   files:typing.Optional[typing.List[UploadFile]] = File( None),
        db: Session = Depends(get_db),current_user: UserCurrent = Depends(
            get_current_active_user)):
    new_users=db.query(Users).filter(Users.id == id).update({
        Users.id: id,
        Users.name: name,
        Users.user_name: user_name,
        Users.roll: roll,
        Users.phone: phone,
        Users.password: get_password_hash(password),

    })
    db.commit()


    if files:
        for file in files:
            with open("media/" + file.filename, 'wb') as image:
                shutil.copyfileobj(file.file, image)
            url = str('media/' + file.filename)
            new_file = Files(
                name=file.filename,
                source_id=id,
                source="user",
                url=url,
                user_id=id

            )
            db.add(new_file)
            db.commit()

    raise HTTPException(status_code=200, detail="Amaliyot muvoffaqiyatli amalga oshirildi")


@user_router.delete("/OCHIRISH")
async def user_delete(id: int, db: Session = Depends(get_db),current_user: UserCurrent = Depends(
            get_current_active_user)):
    return delete_username(id=id, user=current_user, db=db)
