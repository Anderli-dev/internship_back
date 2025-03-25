from db.models.company import Company
from db.models.user import RoleEnum
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.decorators.check_user_role import check_user_role


class CompanyDeleteService:
    @staticmethod
    @check_user_role(role_enum=RoleEnum.owner)
    async def delete_company(db: AsyncSession, company_id: int, user_id: int):
        company = await db.execute(select(Company).filter(Company.id == company_id))
        company = company.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        db.delete(company)
        db.commit()
        return {"detail": "Company deleted"}