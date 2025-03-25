from db.models.company_user_role import CompanyUserRole, RoleEnum
from core.logger import logger
from db.models.company import Company
from db.schemas.company_shema import CompanyCreate
from sqlalchemy.ext.asyncio import AsyncSession


class CompanyCreateService:
    @staticmethod
    async def create_company(db: AsyncSession, company: CompanyCreate, user_id: int) -> Company:
        logger.debug("Creating company")
        company: Company = Company(name=company.name, description=company.description)
        
        logger.debug("Adding company to db")
        db.add(company)
        await db.commit()
        await db.refresh(company)
        
        cur = CompanyUserRole(user_id=user_id, company_id=company.id, role=RoleEnum.owner)
        db.add(cur)
        await db.commit()
        
        return company