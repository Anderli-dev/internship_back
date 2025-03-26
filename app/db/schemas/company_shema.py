from typing import List, Optional

from db.models.company import VisibilityEnum
from pydantic import BaseModel


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
    
class CompaniesListResponse(BaseModel):
    companies: List[CompanyResponse]
    total: int