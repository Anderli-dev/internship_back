from core.logger import logger
from db.models import User
from db.schemas.UserSchema import UserSignUp
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class UserCreateService:
    @staticmethod
    async def create_user(user: UserSignUp, db: AsyncSession) -> User:
        logger.debug("Checking if user exists")
        result = await db.execute(select(User).where((User.email == user.email) | (User.username == user.username)))
        existing_user = result.scalars().first()

        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        logger.debug("Creating user")
        db_user = User(username=user.username, email=user.email, password=user.password)
        
        logger.debug("Adding user to db")
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        
        return db_user