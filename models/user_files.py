from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class user_files(Base):
    __tablename__ = "user_files"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=True)
    user_id = Column(Integer,nullable=True)

