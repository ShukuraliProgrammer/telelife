from fastapi import HTTPException

from models.user_files import user_files


from utils.pagination import pagination


def get_files(search, status, roll, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = user_files.user_id.like(search_formatted) | user_files.file_url.like(search_formatted) | user_files.id.like(
            search_formatted) | user_files.roll.like(search_formatted)
    else:
        search_filter = user_files.id > 0
    if status in [True, False]:
        status_filter = user_files.user_id == status
    else:
        status_filter = user_files.id > 0

    if roll:
        roll_filter = user_files.roll = roll
    else:
        roll_filter = user_files.id > 0

    users = db.query(user_files).filter(search_filter, status_filter, roll_filter).order_by(user_files.user_id.asc())
    if page and limit:
        return pagination(users,page, limit)
    else:
        return users.all()


def add_files(form, user, db):
    user_verification = db.query(user_files).filter(user_files.user_id == form.user_name).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday Foydalanuvchi mavjud")
    number_verification = db.query(user_files).filter(user_files.user_id == form.user_name).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami mavjud")
    if user.roll!="admin":
        raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan")
    new_userfiles = user_files(
        user_id=form.user_id,
        name=form.name,

    )
    db.add(new_userfiles)
    db.commit()


def update_userfiles(form,user, db):
    user_verification = db.query(user_files).filter(user_files.user_id == form.name).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday Foydalanuvchi mavjud")
    number_verification = db.query(user_files).filter(user_files.user_id == form.name).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami mavjud")
    if user.roll != "admin":
        raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan")
    db.query(user_files).filter(user_files.id==form.id).update({
        user_files.id: form.id,
        user_files.user_id: form.user_id,
        user_files.name: form.name

    })
    db.commit()


def delete_userfiles(id,user,db):
    user_verification = db.query(user_files).filter(user_files.id == id).first()
    if not user_verification:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mabjud emas")
    if user.roll != "admin":
        raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan")
    db.query(user_files).filter(user_files.id==id).delete()
    db.commit()

