from fastapi import HTTPException
from sqlalchemy.future import select
from core.settings import logger
from db.models import User
from sqlalchemy.ext.asyncio import AsyncSession

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    users = await db.execute(select(User).offset(skip).limit(limit))
    users = users.scalars().all()
    
    return users

async def get_uses():
    pass

async def create_users():
    pass

async def update_users():
    pass

async def delete_users():
    pass