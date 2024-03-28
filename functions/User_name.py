from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.User_name import Users
from routes.auth import get_password_hash
from utils.pagination import pagination


def get_users(search, status, roll, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Users.name.like(search_formatted) | Users.user_name.like(search_formatted) | Users.id.like(
            search_formatted) | Users.roll.like(search_formatted)
    else:
        search_filter = Users.id > 0
    if status in [True, False]:
        status_filter = Users.status == status
    else:
        status_filter = Users.id > 0

    if roll:
        roll_filter = Users.roll = roll
    else:
        roll_filter = Users.id > 0

    users = db.query(Users).options(joinedload(Users.user_comment)).options(joinedload(Users.user_fallow)).options(joinedload(Users.user_video)).filter(search_filter, status_filter, roll_filter).order_by(Users.name.asc())
    if page and limit:
        return pagination(users,page, limit)
    else:
        return users.all()


def add_username(form, user,db):
    user_verification = db.query(Users).filter(Users.user_name == form.name).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday Foydalanuvchi mavjud")
    number_verification = db.query(Users).filter(Users.phone == form.phone).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami mavjud")
    if user.roll != "admin":
        raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan:(")

    new_users = Users(
        name=form.name,
        user_name=form.user_name,
        roll=form.roll,
        password=get_password_hash(form.password),
        phone=form.phone,

    )
    db.add(new_users)
    db.commit()



def update_username(form, user, db):

    user_verification = db.query(Users).filter(Users.user_name == form.name).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday Foydalanuvchi mavjud")
    number_verification = db.query(Users).filter(Users.user_name == form.name).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami mavjud")
    if user.roll != "admin":
        raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan:(")
    db.query(Users).filter(Users.id == form.id).update({
        Users.id: form.id,
        Users.name: form.name,
        Users.user_name: form.user_name,
        Users.roll: form.roll,
        Users.password: get_password_hash(form.password),

    })
    db.commit()


def delete_username(id, user, db):
    user_verification = db.query(Users).filter(Users.id == id).first()
    if not user_verification:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mabjud emas")
    if user.roll != "admin":
        raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan:(")

    db.query(Users).filter(Users.id == id).delete()
    db.commit()





