from db.models.company_user_role import CompanyUserRole, RoleEnum
from core.logger import logger
from db.models.company import Company
from db.schemas.company_shema import CompanyCreate
from sqlalchemy.ext.asyncio import AsyncSession


class CompanyCreateService:
    @staticmethod
    async def create_company(db: AsyncSession, company: CompanyCreate, user_id: int) -> Company:
        logger.info(f"Starting creation of company: {company.name}")
        
        new_company: Company = Company(name=company.name, description=company.description)
        logger.info("Adding new company instance to the session")
        db.add(new_company)
        await db.commit()
        await db.refresh(new_company)
        logger.info(f"Company created with ID: {new_company.id}")

        logger.info(f"Assigning role 'owner' to user ID {user_id} for company ID {new_company.id}")
        cur = CompanyUserRole(user_id=user_id, company_id=new_company.id, role=RoleEnum.owner)
        db.add(cur)
        await db.commit()
        logger.info("User role assignment committed successfully")

        return new_company
