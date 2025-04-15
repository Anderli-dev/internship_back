from db.models import User
from db.schemas.UserSchema import UserBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.logger import logger


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[UserBase]:
        logger.info("Getting users from db.")
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        users = result.scalars().all()
        return [UserBase.model_validate(user.__dict__) for user in users]

    async def get_user(self, user_id: int) -> User | None:
        logger.info("Getting user from db by id.")
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()
    
    async def get_user_by_email(self, user_email: str):
        logger.info("Getting user from db by email.")
        result = await self.db.execute(select(User).filter(User.email == user_email))
        return result.scalars().first()
    
    async def create(self, user_data: dict) -> User:
        logger.info("Creating user in db.")
        db_user = User(**user_data)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user
    
    async def update(self, user_id: int, user_data: dict) -> User | None:
        logger.info("Updating user in db.")
        result = await self.db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if not user:
            return None

        for key, value in user_data.items():
            setattr(user, key, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        logger.info("Deleting user in db.")
        result = await self.db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if not user:
            return False

        await self.db.delete(user)
        await self.db.commit()
        return True
