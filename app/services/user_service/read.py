from core.logger import logger
from db.models import User
from db.schemas.user_schema import UserBase
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.decorators.user_action_error_check import user_action_error_check


class UserReadService:
    @staticmethod
    async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[UserBase]:
        logger.debug("Getting all users")
        print(type(db))
        users = await db.execute(select(User).offset(skip).limit(limit))
        users = users.scalars().all()
        users = [UserBase.model_validate(user.__dict__) for user in users] # Creating list of UserBase
        
        return users
    
    @staticmethod
    async def get_user_by_field(db: AsyncSession, field: str, value) -> User:
        logger.debug("Getting user")
        user = await db.execute(select(User).filter(getattr(User, field) == value))
        user = user.scalars().first()
        
        if not user:
            logger.error("User not found!")
            raise HTTPException(status_code=404, detail="User not found!")
        
        return user

    @user_action_error_check(secur=True)
    async def read_auth_user(self, db: AsyncSession, payload: dict, user: User) -> User:
        return user
    
    async def read_user_from_db(self, db: AsyncSession, user_id: int) -> User:
        user = await self.get_user_by_field(db, "id", user_id)
        if not user:
            logger.error("User not found!")
            raise HTTPException(status_code=404, detail="User not found!")
        return user