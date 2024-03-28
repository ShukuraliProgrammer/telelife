from sqlalchemy import Column, Integer, String, Boolean, Float, Text, DATETIME
from sqlalchemy.orm import relationship

from db import Base


class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    last_name = Column(String(70), nullable=True)
    user_name = Column(String(70), unique=True, nullable=False)
    roll = Column(String(30), nullable=True)
    bio = Column(String(80), nullable=True)
    phone = Column(String(20), nullable=True)
    password = Column(String(50), nullable=True)
    token = Column(String(400), default='', nullable=True)
    status = Column(Boolean, nullable=False, default=True)
    create_at = Column(DATETIME, nullable=True)

    user_comment = relationship('Users_comment', back_populates='user')
    user_fallow = relationship('users_followers', back_populates='fallow')
    user_video = relationship('Video', back_populates='video')