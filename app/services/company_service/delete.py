from db.models.company_user_role import CompanyUserRole, RoleEnum
from db.models.company import Company
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import delete
from utils.decorators.check_user_role import check_user_role
from core.logger import logger

class CompanyDeleteService:
    @staticmethod
    @check_user_role(role_enum=RoleEnum.owner)
    async def delete_company(db: AsyncSession, company_id: int, user_id: int) -> dict:
        logger.info(f"User ID {user_id} initiated deletion of company ID {company_id}")

        logger.info(f"Removing company-user role links for company ID {company_id}")
        await db.execute(delete(CompanyUserRole).where(CompanyUserRole.company_id == company_id))

        logger.info(f"Fetching company with ID {company_id} from the database")
        company = await db.execute(select(Company).filter(Company.id == company_id))
        company: Company = company.scalars().first()

        if not company:
            logger.info(f"Company with ID {company_id} not found")
            raise HTTPException(status_code=404, detail="Company not found")

        logger.info(f"Deleting company with ID {company_id}")
        await db.delete(company)
        await db.commit()
        logger.info(f"Company with ID {company_id} deleted successfully by user ID {user_id}")

        return {"detail": "Company deleted"}
