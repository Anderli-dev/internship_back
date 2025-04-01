from core.logger import logger
from db.models import User
from db.schemas.UserSchema import UserBase, UserSignUp, UserUpdate
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 10) -> list[User]:
        logger.debug("Getting all users")
        users = await self.db.execute(select(User).offset(skip).limit(limit))
        users = users.scalars().all()
        users = [UserBase.model_validate(user.__dict__) for user in users] # Creating list of UserBase
        
        return users

    async def get_user(self, user_id: int) -> User:
        logger.debug("Getting user")
        user = await self.db.execute(select(User).filter(User.id == user_id))
        user = user.scalars().first()
        
        return user

    async def create(self, user: UserSignUp) -> User: 
        logger.debug("Creating user")
        db_user = User(username=user.username, email=user.email, password=user.password)
        
        logger.debug("Adding user to db")
        await self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        
        return db_user

    async def update(self, user_id: int, user_data: UserUpdate) -> User:
        logger.debug("Updating user")
        user = await self.db.execute(select(User).filter(User.id == user_id))
        user = user.scalars().first()
        
        logger.debug("Setting up user data")
        # Updating not None fields
        for key, data in user_data.items():
            setattr(user, key, data)
        
        logger.debug("Saving new user data in db")
        await self.db.commit()
        await self.db.refresh(user)
        
        return user

    async def delete(self, user_id: int) -> bool:
        logger.debug("Looking for user to delete")
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        if not user:
            logger.debug(f"User with ID {user_id} not found")
            return False

        logger.debug(f"Deleting user with ID {user_id}")
        await self.db.delete(user)
        await self.db.commit()

        return True