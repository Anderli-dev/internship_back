from core.logger import logger
from db.models.company import Company
from db.models.user import User
from db.schemas.company_shema import (CompaniesListResponse, CompanyCreate,
                                      CompanyResponse, CompanyUpdate)
from db.session import get_db
from fastapi import APIRouter, Depends, Response
from services.auth import Auth
from services.company_service.create import CompanyCreateService
from services.company_service.delete import CompanyDeleteService
from services.company_service.read import CompanyReadService
from services.company_service.update import CompanyUpdateService
from services.user_service.read import UserReadService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.get("/", response_model=CompaniesListResponse)
async def get_all_companies(db: AsyncSession = Depends(get_db)) -> CompaniesListResponse:
    logger.info("Fetching all companies from the database")
    companies: list[Company] = await CompanyReadService.get_all_companies(db)
    total: int = len(companies)
    if not total:
        logger.debug("No companies in db!")
        return Response(status_code=204)
    logger.info(f"Total companies fetched: {total}")
    
    return CompaniesListResponse.model_validate({"companies": companies, "total": total})


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: int, db: AsyncSession = Depends(get_db)) -> CompanyResponse:
    logger.info(f"Fetching company with ID: {company_id}")
    company: Company = await CompanyReadService().read_company_from_db(db, company_id)
    logger.info(f"Company with ID {company_id} fetched successfully")
    return company


@router.post("/", response_model=CompanyResponse)
async def create_company(company_data: CompanyCreate, db: AsyncSession = Depends(get_db), payload: dict = Depends(Auth().get_token_payload)) -> CompanyResponse:
    logger.info("Creating a new company")
    user: User = await UserReadService().read_auth_user(db, payload=payload)
    logger.info(f"Authenticated user ID: {user.id}")
    
    company: Company = await CompanyCreateService.create_company(db, company_data, user.id)
    logger.info(f"Company created successfully with user ID {user.id}")
    if company is None:
        logger.error("Company creation failed!")
        return Response(status_code=204, detail="Company creation failed!")
    return company


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(company_id: int, company_data: CompanyUpdate, db: AsyncSession = Depends(get_db), payload: dict = Depends(Auth().get_token_payload)) -> CompanyResponse:
    logger.info(f"Updating company with ID: {company_id}")
    user: User = await UserReadService().read_auth_user(db, payload=payload)
    logger.info(f"Authenticated user ID: {user.id}")

    updated_company: Company = await CompanyUpdateService.update_company(db, company_id, company_data, user_id=user.id)
    logger.info(f"Company with ID {company_id} updated successfully by user ID {user.id}")
    return updated_company


@router.delete("/{company_id}")
async def delete_company(company_id: int, db: AsyncSession = Depends(get_db), payload: dict = Depends(Auth().get_token_payload)) -> dict:
    logger.info(f"Deleting company with ID: {company_id}")
    user: User = await UserReadService().read_auth_user(db, payload=payload)
    logger.info(f"Authenticated user ID: {user.id}")

    result: dict = await CompanyDeleteService.delete_company(db, company_id, user_id=user.id)
    logger.info(f"Company with ID {company_id} deleted successfully by user ID {user.id}")
    return result
