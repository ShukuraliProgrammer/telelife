from fastapi import HTTPException, exception_handlers
from sqlalchemy.orm import joinedload

from models.video import Video, VideoLike


from utils.pagination import pagination


def get_video(search, status, roll, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Video.name.like(search_formatted) | Video.user_id.like(search_formatted) | Video.create_at.like(
            search_formatted) | Video.roll.like(search_formatted)
    else:
        search_filter = Video.id > 0
    if status in [True, False]:
        status_filter = Video.status == status
    else:
        status_filter = Video.id > 0

    if roll:
        roll_filter = Video.roll = roll
    else:
        roll_filter = Video.id > 0

    users = db.query(Video).options(joinedload(Video.video)).options(joinedload(Video.comment_video)).filter(search_filter, status_filter, roll_filter).order_by(Video.name.asc())
    if page and limit:
        return pagination(users,page, limit)
    else:
        return users.all()


def add_uservideo(form, user, db):

    user_verification = db.query(Video).filter(Video.user_name == form.user_name).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday Foydalanuvchi mavjud")
    number_verification = db.query(Video).filter(Video.user_name == form.user_name).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami mavjud")
    if user.roll!="admin":
        raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan")
    new_uservideo = Video(

        user_id=form.user_id,
        name=form.name,


    )
    db.add(new_uservideo)
    db.commit()


def add_likevideo(form, user, db):
    user_verification = db.query(Video).filter(Video.user_name == form.user_name).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday Foydalanuvchi mavjud")
    number_verification = db.query(Video).filter(Video.user_name == form.user_name).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami mavjud")
    if user.roll != "admin":
        raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan")
    new_likervideo = Video(

        user_id=form.user_id,
        like_number=form.like_number

    )
    db.add(new_likervideo)
    db.commit()


def update_uservideo(form,user, db):
    user_verification = db.query(Video).filter(Video.user_name == form.user_name).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday Foydalanuvchi mavjud")
    number_verification = db.query(Video).filter(Video.user_name == form.user_name).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami mavjud")
    if user.roll!="admin":
        raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan")
    db.query(Video).filter(Video.id == form.id).update({
        Video.id: form.id,
        Video.user_id: form.user_id,
        Video.name: form.name,
        Video.janr: form.janr

    })
    db.commit()


def delete_uservideo(id, user,db):
    user_verification = db.query(Video).filter(Video.id == id).first()
    if not user_verification:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mabjud emas")
    if user.roll!="admin":
        raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan")
    db.query(Video).filter(Video.id == id).delete()
    db.commit()



def create_videolike(video_id, user, db):

    try:
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            return HTTPException(status_code=400, detail="Bunday video mavjud emas")
        
        video_like = db.query(VideoLike).filter(VideoLike.user_id == user.id, VideoLike.video_id == video.id).first()
        if video_like and video_like.id:
            return HTTPException(status_code=400, detail="Siz allaqachon like qo'ygan ekansiz")
        
        new_likervideo = VideoLike(
            user_id=user.id,
            video_id=video_id,
        )
        db.add(new_likervideo)
        db.commit()
        db.refresh(new_likervideo)
        return new_likervideo
    except Exception as e:
        print(e)
        return HTTPException(status_code=400, detail="Xatolik yuz berdi")