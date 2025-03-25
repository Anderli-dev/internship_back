from pydantic import BaseModel
from typing import Optional
from db.models.company import VisibilityEnum

class CompanyResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    visibility: VisibilityEnum
    
class CompanyCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    visibility: Optional[VisibilityEnum] = None