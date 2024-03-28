import shutil
import typing
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from functions.user_files import get_files, add_files, update_userfiles, delete_userfiles
from db import get_db
from models.files import Files
from models.user_files import user_files
from routes.auth import get_current_active_user
from schemas.Users_name import UserCurrent
from schemas.user_files import filesUpdate, filesCreate
from models.User_name import Users

files_router = APIRouter()


@files_router.get("", status_code=200)
async def get_all_users(search: str = None, status: bool = True, roll: str = None, page: int = 1,
                        limit: int = 25,
                        db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):
    return get_files(search=search, status=status,roll=roll, page=page, limit=limit, db=db)


@files_router.post("/add")
async def user_add(name: str,

                   files: typing.Optional[list[UploadFile]] = File(None),
                   db: Session = Depends(get_db),current_user: UserCurrent = Depends(
            get_current_active_user)):
    new_userfiles = user_files(
        user_id=current_user.id,
        name=name,

    )
    db.add(new_userfiles)
    db.commit()

    if files:
        for file in files:
            with open("media/" + file.filename, 'wb') as image:
                shutil.copyfileobj(file.file, image)
            url = str('media/' + file.filename)
            new_filesesss = Files(
                name=file.filename,
                source_id=new_userfiles.id,
                source="user",
                url=url,
                user_id=current_user.id
            )
            db.add(new_filesesss)
            db.commit()

    raise HTTPException(status_code=200, detail="Amaliyot muvofaqiyatli amalga oshirildi")


@files_router.put("/update")
async def user_update(id: int,
                      name: str,

                      files: typing.Optional[list[UploadFile]] = File(None),
        db: Session = Depends(get_db),current_user: UserCurrent = Depends(
            get_current_active_user)):
    new_update=db.query(user_files).filter(user_files.id == id).update({
        user_files.id: id,
        user_files.user_id: current_user.id,
        user_files.name: name

    })
    db.add(new_update)
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

    raise HTTPException(status_code=200, detail="Amaliyot muvofaqiyatli amalga oshirildi")


@files_router.delete("/delete")
async def user_delete(id: int, db: Session = Depends(get_db),current_user: UserCurrent = Depends(
            get_current_active_user)):
    return delete_userfiles(id=id, user=current_user,db=db)
