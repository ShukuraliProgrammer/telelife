from sqlalchemy import Column, Integer, String, Boolean,DATETIME, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class Video(Base):
    __tablename__ = "Video"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"),nullable=True)
    name = Column(String(50), nullable=False)
    like_number = Column(Integer, nullable=True)
    janr = Column(String(50), nullable=True)
    dislike_number = Column(Integer, nullable=True)
    comment_number = Column(Integer, nullable=True)
    vuews_number = Column(Integer, nullable=True)
    status = Column(Boolean, nullable=False, default=True)
    create_at = Column(DATETIME, nullable=True)

    video = relationship("Users", back_populates='user_video')
    comment_video = relationship("Users_comment", back_populates='video_comment')



class VideoLike(Base):
    __tablename__ = "VideoLike"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"),nullable=True)
    video_id = Column(Integer, ForeignKey("Video.id"),nullable=True)
   


