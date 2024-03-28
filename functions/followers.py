from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.followers import users_followers


from utils.pagination import pagination


def get_folowers(search, status, roll, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = users_followers.name.like(search_formatted) | users_followers.user_id.like(search_formatted) | users_followers.create_at.like(
            search_formatted) | users_followers.roll.like(search_formatted)
    else:
        search_filter = users_followers.id > 0
    if status in [True, False]:
        status_filter = users_followers.status == status
    else:
        status_filter = users_followers.id > 0

    if roll:
        roll_filter = users_followers.roll = roll
    else:
        roll_filter = users_followers.id > 0

    users = db.query(users_followers).options(joinedload(users_followers.fallow)).filter(search_filter, status_filter, roll_filter)
    if page and limit:
        return pagination(users,page, limit)
    else:
        return users.all()


def add_userfollowers(form,user, db):
    user_verification = db.query(users_followers).filter(users_followers.user_name == form.user_name).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday Foydalanuvchi mavjud")
    number_verification = db.query(users_followers).filter(users_followers.user_name == form.user_name).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami mavjud")
    if user.roll!="admin":
        raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan")
    new_userfollowers = users_followers(
        user_id=form.user_id,
        follower_id=form.follower_id,



    )
    db.add(new_userfollowers)
    db.commit()


def update_userfollowers(form, user,db):
    user_verification = db.query(users_followers).filter(users_followers.user_name == form.user_name).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday Foydalanuvchi mavjud")
    number_verification = db.query(users_followers).filter(users_followers.user_name == form.user_name).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami mavjud")
    if user.roll!="admin":
        raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan")
    db.query(users_followers).filter(users_followers.id==form.id).update({
        users_followers.id: form.id,
        users_followers.user_id: form.user_id,
        users_followers.follower_id: form.follower_id,

    })
    db.commit()

#@dikofx_admin

def delete_userupdate(id, user,db):
    user_verification = db.query(users_followers).filter(users_followers.id == id).first()
    if not user_verification:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mabjud emas")
    if user.roll!="admin":
        raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan")
    db.query(users_followers).filter(users_followers.id == id).delete()
    db.commit()

