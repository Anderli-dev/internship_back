from enum import Enum

from app.db.base import BaseModel
from sqlalchemy import Column
from sqlalchemy import Enum as SAEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship


class RoleEnum(Enum):
    owner = "owner"
    admin = "admin"
    member = "member"
    viewer = "viewer"

class User(BaseModel):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=True)

    company = relationship("Company", back_populates="owner")
    role = Column(SAEnum(RoleEnum), default=RoleEnum.viewer, nullable=False)