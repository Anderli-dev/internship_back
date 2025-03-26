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
        logger.info(f"Fetching companies from DB with skip={skip}, limit={limit}")
        
        companies = await db.execute(select(Company).offset(skip).limit(limit))
        companies: Company = companies.scalars().all()
        logger.info(f"Retrieved {len(companies)} companies from database")

        companies: list[Company] = [CompanyResponse.model_validate(company.__dict__) for company in companies]
        logger.info("Transformed raw company data to CompanyResponse schema list")
        
        return companies

    @staticmethod
    async def get_company_by_field(db: AsyncSession, field: str, value) -> Company:
        logger.info(f"Fetching company where {field} = {value}")
        
        company = await db.execute(select(Company).filter(getattr(Company, field) == value))
        company: Company = company.scalars().first()
        
        if not company:
            logger.error(f"Company not found with {field} = {value}")
            raise HTTPException(status_code=404, detail="Company not found!")
        
        logger.info(f"Company found with {field} = {value}")
        return company

    async def read_company_from_db(self, db: AsyncSession, company_id: int) -> Company:
        logger.info(f"Reading company with ID: {company_id}")
        
        company: Company = await self.get_company_by_field(db, "id", company_id)
        
        if not company:
            logger.error(f"Company with ID {company_id} not found")
            raise HTTPException(status_code=404, detail="Company not found!")

        logger.info(f"Company with ID {company_id} retrieved successfully")
        return company
