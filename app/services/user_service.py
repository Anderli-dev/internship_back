from fastapi import HTTPException
from sqlalchemy.future import select
from core.settings import logger
from db.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.UserSchema import UserBase, UserSignUp

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    users = await db.execute(select(User).offset(skip).limit(limit))
    users = users.scalars().all()
    users = [UserBase.model_validate(user.__dict__) for user in users]
    
    return users

async def read_user(user_id: int, db: AsyncSession):
    user = await db.execute(select(User).filter(User.id == user_id))
    user = user.scalars().first()
    
    return user

async def create_new_user(user: UserSignUp, db: AsyncSession):
    db_user = User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user():
    pass

async def delete_user():
    pass