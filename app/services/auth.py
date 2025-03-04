import asyncio
from datetime import datetime, timedelta
from typing import Optional

import jwt
from core.settings import SECRET_KEY, logger
from db.models import User
from fastapi import HTTPException
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.hash_password import verify_password

ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

async def authenticate_user(user_email: str, password: str, db: AsyncSession):
    user = await db.execute(select(User).filter(User.email == user_email))
    user = user.scalars().first()
    
    if not user or not verify_password(password, user.password):
        logger.error("User not found!")
        raise HTTPException(status_code=404, detail="User not found!")
    
    return user

async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    
    loop = asyncio.get_running_loop()
    encoded_jwt = await loop.run_in_executor(None, jwt.encode, to_encode, SECRET_KEY, ALGORITHM)
    
    return encoded_jwt