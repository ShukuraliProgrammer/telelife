from sqlalchemy import Column, Integer, String, Boolean, Float, Text
from sqlalchemy_utils import URLType
from sqlalchemy.orm import relationship
from db import Base


class Files(Base):
    __tablename__ = "Files"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=True)
    source_id = Column(Integer, nullable=True)
    source = Column(String(30), nullable=True)
    url = Column(URLType, nullable=True)
    user_id = Column(Integer, nullable=False)


