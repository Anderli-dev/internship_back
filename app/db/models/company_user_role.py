from db.base import BaseModel
from db.models.user import RoleEnum
from sqlalchemy import Column
from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, Integer


class CompanyUserRole(BaseModel):
    __tablename__ = "company_user_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    role = Column(SAEnum(RoleEnum), default=RoleEnum.viewer, nullable=False)