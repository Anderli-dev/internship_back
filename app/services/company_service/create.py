
from core.logger import logger
from db.models.company import Company
from db.schemas.company_shema import CompanyCreate
from sqlalchemy.ext.asyncio import AsyncSession


class CompanyCreateService:
    @staticmethod
    async def create_company( db: AsyncSession, company: CompanyCreate, user_id: int) -> Company:
        logger.debug("Creating company")
        company = Company(name=company.name, description=company.description, owner_id=user_id)
        
        logger.debug("Adding user to db")
        db.add(company)
        await db.commit()
        await db.refresh(company)
        
        return company