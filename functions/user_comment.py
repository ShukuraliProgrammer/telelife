from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.user_comment import Users_comment


from utils.pagination import pagination


def get_comment(search, status, roll, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Users_comment.user_id.like(search_formatted) | Users_comment.id.like(search_formatted) | Users_comment.video_id.like(
            search_formatted) | Users_comment.roll.like(search_formatted)
    else:
        search_filter = Users_comment.id > 0
    if status in [True, False]:
        status_filter = Users_comment.status == status
    else:
        status_filter = Users_comment.id > 0

    if roll:
        roll_filter = Users_comment.roll = roll
    else:
        roll_filter = Users_comment.id > 0

    users = db.query(Users_comment).options(joinedload(Users_comment.user)).options(joinedload(Users_comment.video_comment)).filter(search_filter, status_filter, roll_filter).order_by(Users_comment.video_id.asc())
    if page and limit:
        return pagination(users,page, limit)
    else:
        return users.all()


def add_usercomment(form, user,db):
    user_verification = db.query(Users_comment).filter(Users_comment.user_name == form.user_name).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday Foydalanuvchi mavjud")
    number_verification = db.query(Users_comment).filter(Users_comment.user_name == form.user_name).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami mavjud")
    if user.roll!="admin":
        raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan")
    new_user_comment = Users_comment(
        user_id=form.user_id,
        video_id=form.video_id,

    )
    db.add(new_user_comment)
    db.commit()


def update_usercomment(form, user,db):
    user_verification = db.query(Users_comment).filter(Users_comment.user_name == form.user_name).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday Foydalanuvchi mavjud")
    number_verification = db.query(Users_comment).filter(Users_comment.user_name == form.user_name).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami mavjud")
    if user.roll!="admin":
        raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan")
    db.query(Users_comment).filter(Users_comment.id==form.id).update({
        Users_comment.id: form.id,
        Users_comment.user_id: form.user_id,
        Users_comment.video_id: form.video_id,
    }
    )
    db.commit()


def delete_usercomment(id,user, db):
    user_verification = db.query(Users_comment).filter(Users_comment.id == id).first()
    if not user_verification:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mabjud emas")
    if user.roll!="admin":
        raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan")
    db.query(Users_comment).filter(Users_comment.id==id).delete()
    db.commit()

