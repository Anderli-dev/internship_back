from enum import Enum

from sqlalchemy import Column
from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, Integer

from db.base import BaseModel


class RoleEnum(Enum):
    owner = "owner"
    admin = "admin"
    member = "member"
    viewer = "viewer"

class CompanyUserRole(BaseModel):
    __tablename__ = "company_user_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    role = Column(SAEnum(RoleEnum), default=RoleEnum.viewer, nullable=False)