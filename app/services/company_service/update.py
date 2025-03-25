from core.logger import logger
from db.models import User
from db.models.company import Company
from db.models.user import RoleEnum
from db.schemas.company_shema import CompanyUpdate
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class CompanyUpdateService:
    @staticmethod
    async def update_company(db: AsyncSession, company_id: int, company_data: CompanyUpdate, user_id: int):
        access = check_user_role(db, user_id, RoleEnum.owner)
        if not access:
            raise HTTPException(status_code=403, detail="Only the Owner can update the company")

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
    
async def check_user_role(db: AsyncSession, user_id: int, role_enum: RoleEnum) -> bool:
    user = await db.execute(select(User).filter(User.id == user_id))
    user = user.scalars().first()
    
    if not user:
        logger.error("User not found!")
        raise HTTPException(status_code=404, detail="User not found!")
    
    return user.role == role_enum