from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm.session import Session

from schemas.login import TokenData
from db import get_db
from schemas.Users_name import UserCurrent

from models.user_comment import Users_comment
from models.user_files import user_files
from models.followers import users_followers
from models.User_name import Users

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 8600000

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

login_router = APIRouter()


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=402, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("sub")
        if user_name is None:
            raise credentials_exception
        token_data = TokenData(username=user_name)
    except JWTError:
        raise credentials_exception
    user = db.query(Users).where(Users.user_name == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserCurrent = Depends(get_current_user)):
    if current_user.status:
        return current_user
    raise HTTPException(status_code=400, detail="Inactive user")


@login_router.post("/token")
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(Users).where(Users.user_name == form_data.username, Users.status == True).first()
    if user:
        is_validate_password = pwd_context.verify(form_data.password, user.password)
    else:
        is_validate_password = False
    if not is_validate_password:
        raise HTTPException(status_code=400, detail="Login yoki parolda xatolik")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )
    db.query(Users).filter(Users.user_name == form_data.username).update({
        Users.token: access_token
    })
    db.commit()
    return {'id': user.id, "access_token": access_token, "roll": user.roll}






