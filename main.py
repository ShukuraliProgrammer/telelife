from fastapi import FastAPI

from routes import auth, User_name, video, comment, followers, users_files

from db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Shablon",
    responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
               401: {'desription': 'Unauthorized'}}
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return {"message": "telelife"}


app.include_router(
    auth.login_router,
    prefix='/auth',
    tags=['User auth section'])

app.include_router(
    User_name.user_router,
    prefix='/User',
    tags=['User section'])

app.include_router(
    comment.comment_router,
    prefix='/comment',
    tags=['comment section'])

app.include_router(
    followers.followers_router,
    prefix='/followers',
    tags=['followers section'])

# app.include_router(
#     users_files.files_router,
#     prefix='/users_files',
#     tags=['users_files section'])

app.include_router(
    video.video_router,
    prefix='/Video',
    tags=['video section'])
