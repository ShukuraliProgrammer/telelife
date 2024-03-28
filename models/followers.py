from sqlalchemy import Column, Integer, String, Boolean, Float, Text, DATETIME, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class users_followers(Base):
    __tablename__ = "users_followers"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,ForeignKey("Users.id"),nullable=True)
    follower_id = Column(Integer,ForeignKey("Files.id"),nullable=True)
    status = Column(Boolean, nullable=False, default=True)
    create_at = Column(DATETIME, nullable=True)

    fallow = relationship("Users", back_populates='user_fallow')

