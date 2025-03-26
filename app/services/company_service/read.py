from db.schemas.company_shema import CompanyResponse
from core.logger import logger
from db.models.company import Company
from db.schemas.user_schema import UserBase
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.decorators.user_action_error_check import user_action_error_check


class CompanyReadService:
    @staticmethod
    async def get_all_companies(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[CompanyResponse]:
        logger.debug("Getting all companies")
        
        companies = await db.execute(select(Company).offset(skip).limit(limit))
        companies = companies.scalars().all()
        companies = [CompanyResponse.model_validate(company.__dict__) for company in companies] # Creating list of companies
        
        return companies
    
    @staticmethod
    async def get_company_by_field(db: AsyncSession, field: str, value) -> Company:
        logger.debug("Getting user")
        company = await db.execute(select(Company).filter(getattr(Company, field) == value))
        company = company.scalars().first()
        
        if not company:
            logger.error("Company not found!")
            raise HTTPException(status_code=404, detail="Company not found!")
        
        return company
    
    async def read_company_from_db(self, db: AsyncSession, company_id: int) -> Company:
        company = await self.get_company_by_field(db, "id", company_id)
        if not company:
            logger.error("Company not found!")
            raise HTTPException(status_code=404, detail="Company not found!")
        return company