import functools

from core.logger import logger
from db.models import User
from db.models.company_user_role import CompanyUserRole, RoleEnum
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


def check_user_role(role_enum: RoleEnum):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(
            db: AsyncSession,
            *args,
            **kwargs
        ):                
            print(args)
            if not kwargs.get("user_id"):
                logger.error("User id missing")
                raise HTTPException(status_code=400, detail="Invalid user ID")
                
            user = await db.execute(select(CompanyUserRole).filter(CompanyUserRole.user_id == kwargs["user_id"]))
            user: User = user.scalars().first()
            
            if not user:
                logger.error("Company with user not found!")
                raise HTTPException(status_code=404, detail="Company with user not found!")
            
            if not user.role == role_enum:
                raise HTTPException(status_code=403, detail=f"Only the {role_enum} can update the company")
            
            return await func(db, *args, **kwargs)

        return wrapper
    return decorator