from enum import Enum

from db.base import BaseModel
from sqlalchemy import Column
from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class VisibilityEnum(Enum):
    hidden = "hidden"
    visible = "visible"
    
class Company(BaseModel):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    visibility = Column(SAEnum(VisibilityEnum), default=VisibilityEnum.hidden, nullable=False)
    
    owner = relationship("User", back_populates="company")
    