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
        company = await db.execute(select(Company).filter(Company.id == company_id))
        company = company.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        logger.debug("Setting up company data")
        for key, data in company_data.model_dump(exclude_unset=True).items():
            setattr(company, key, data)
        
        logger.debug("Saving company data in db")
        
        await db.commit()
        await db.refresh(company)

        return company
    
