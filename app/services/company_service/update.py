from db.models.company_user_role import RoleEnum
from core.logger import logger
from db.models.company import Company
from db.schemas.company_shema import CompanyUpdate
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.decorators.check_user_role import check_user_role


class CompanyUpdateService:
    @staticmethod
    @check_user_role(role_enum=RoleEnum.owner)
    async def update_company(db: AsyncSession, company_id: int, company_data: CompanyUpdate, user_id: int):
        logger.info(f"User ID {user_id} initiated update for company ID {company_id}")

        company_result = await db.execute(select(Company).filter(Company.id == company_id))
        company: Company = company_result.scalars().first()

        if not company:
            logger.error(f"Company with ID {company_id} not found")
            raise HTTPException(status_code=404, detail="Company not found")

        logger.info(f"Updating company ID {company_id} with new data")

        for key, data in company_data.model_dump(exclude_unset=True).items():
            logger.debug(f"Updating field '{key}' to '{data}'")
            setattr(company, key, data)

        await db.commit()
        await db.refresh(company)

        logger.info(f"Company with ID {company_id} updated successfully by user ID {user_id}")

        return company
