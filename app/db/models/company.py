from enum import Enum

from sqlalchemy import Column
from sqlalchemy import Enum as SAEnum
from sqlalchemy import Integer, String

from db.base import BaseModel


class VisibilityEnum(Enum):
    hidden = "hidden"
    visible = "visible"
    
class Company(BaseModel):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    visibility = Column(SAEnum(VisibilityEnum), default=VisibilityEnum.hidden, nullable=False)
    