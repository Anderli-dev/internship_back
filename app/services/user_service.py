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
        
        if not user:
            logger.error("User not found!")
            raise HTTPException(status_code=404, detail="User not found!")
        
        return user

    async def create(self, user: UserSignUp) -> User:
        logger.debug("Checking if user exists")
        result = await self.db.execute(select(User).where((User.email == user.email) | (User.username == user.username)))
        existing_user = result.scalars().first()

        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email or username already exists")
        
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

    async def delete(self, user_id: int) -> None:
        logger.debug("Deleting user")
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        logger.debug("Deleting user in db")
        await self.db.delete(user)
        await self.db.commit()

        return {"message": "User deleted successfully"}