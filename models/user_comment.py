from sqlalchemy import Column, Integer, String, Boolean, Float, Text, DATETIME, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class Users_comment(Base):
    __tablename__ = "Users_comment"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,ForeignKey("Users.id"),nullable=True)
    video_id = Column(Integer,ForeignKey("Video.id"),nullable=True)
    status = Column(Boolean, nullable=False, default=True)
    create_at = Column(DATETIME, nullable=True)

    user = relationship("Users", back_populates="user_comment")
    video_comment = relationship("Video", back_populates="comment_video")
