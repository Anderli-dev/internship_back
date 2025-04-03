from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.logger import logger
from db.models import User
from db.schemas.UserSchema import UserBase, UserSignUp, UserUpdate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[UserBase]:
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        users = result.scalars().all()
        return [UserBase.model_validate(user.__dict__) for user in users]

    async def get_user(self, user_id: int) -> User | None:
        result = await self.db.execute(
            select(User).filter(User.id == user_id)
        )
        return result.scalars().first()

    async def create(self, user: UserSignUp) -> User:
        db_user = User(**user.model_dump())
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user
    
    async def update(self, user_id: int, user_update: UserUpdate) -> User | None:
        result = await self.db.execute(
            select(User).filter(User.id == user_id)
        )
        user = result.scalars().first()
        if not user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        result = await self.db.execute(
            select(User).filter(User.id == user_id)
        )
        user = result.scalars().first()
        if not user:
            return False

        await self.db.delete(user)
        await self.db.commit()
        return True
