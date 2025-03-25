from db.models.user import User
from db.session import get_db
from fastapi import APIRouter, Depends
from services.auth import Auth
from services.company_service.create import CompanyCreateService
from services.user_service.read import UserReadService
from sqlalchemy.ext.asyncio import AsyncSession

from db.schemas.company_shema import CompanyCreate, CompanyResponse

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.post("/", response_model=CompanyResponse)
async def create_company_endpoint(company_data: CompanyCreate, db: AsyncSession = Depends(get_db), payload: dict = Depends(Auth().get_token_payload)):
    user: User = await UserReadService().read_auth_user(db, payload=payload)
    
    return await CompanyCreateService.create_company(db, company_data, user.id)