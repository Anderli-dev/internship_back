from db.models.user import User
from db.schemas.company_shema import (CompanyCreate, CompanyResponse,
                                      CompanyUpdate)
from db.session import get_db
from fastapi import APIRouter, Depends
from services.auth import Auth
from services.company_service.create import CompanyCreateService
from services.company_service.delete import CompanyDeleteService
from services.company_service.update import CompanyUpdateService
from services.user_service.read import UserReadService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.post("/", response_model=CompanyResponse)
async def create_company_endpoint(company_data: CompanyCreate, db: AsyncSession = Depends(get_db), payload: dict = Depends(Auth().get_token_payload)):
    user: User = await UserReadService().read_auth_user(db, payload=payload)
    
    return await CompanyCreateService.create_company(db, company_data, user.id)

@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company_endpoint(company_id: int, company_data: CompanyUpdate, db: AsyncSession = Depends(get_db), payload: dict = Depends(Auth().get_token_payload)):
    user: User = await UserReadService().read_auth_user(db, payload=payload)
    
    return await CompanyUpdateService.update_company(db, company_id, company_data, user_id=user.id)

@router.delete("/{company_id}")
async def delete_company_endpoint(company_id: int, db: AsyncSession = Depends(get_db), payload: dict = Depends(Auth().get_token_payload)):
    user: User = await UserReadService().read_auth_user(db, payload=payload)
    
    return await CompanyDeleteService.delete_company(db, company_id, user_id=user.id)