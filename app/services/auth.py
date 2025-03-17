import asyncio
from datetime import datetime, timedelta
from typing import Optional

from core.logger import logger
from core.settings import settings
from db.models import User
from fastapi import HTTPException, Security, security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import exceptions, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.hash_password import verify_password

ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

async def authenticate_user(user_email: str, password: str, db: AsyncSession) -> User:
    logger.info("User authentication.")
    user = await db.execute(select(User).filter(User.email == user_email))
    user = user.scalars().first()
    
    if not user or not verify_password(password, user.password):
        logger.error("User not found!")
        raise HTTPException(status_code=404, detail="User not found!")
    
    logger.info("User authentication success.")
    return user

async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    logger.info("Creating token.")
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    
    loop = asyncio.get_running_loop()
    encoded_jwt = await loop.run_in_executor(None, jwt.encode, to_encode, settings.secret_key, settings.jwt_algorithm)
    
    logger.info("Token creation success.")
    return encoded_jwt

security = HTTPBearer()

async def verify_jwt(db: AsyncSession, credentials: HTTPAuthorizationCredentials = Security(security)) -> User:
    logger.debug("Getting user by token")
    try:
        token = credentials.credentials
        
        loop = asyncio.get_running_loop()
        decoded_jwt = await loop.run_in_executor(None, jwt.decode, token, settings.secret_key, settings.jwt_algorithm)
        
        user_email = decoded_jwt.get("user_email")
        if user_email is None:
            logger.error("Invalid token!")
            raise HTTPException(status_code=401, detail="Invalid token!")
        
        user = await db.execute(select(User).filter(User.email == decoded_jwt.get("user_email")))
        user = user.scalars().first()
        
        if not user:
            logger.error("User not found!")
            raise HTTPException(status_code=404, detail="User not found!")
        
        return user
    except exceptions.ExpiredSignatureError:
        logger.error("Token expired!")
        raise HTTPException(status_code=401, detail="Token expired!")
    except exceptions.JWEInvalidAuth:
        logger.error("Invalid token!")
        raise HTTPException(status_code=401, detail="Invalid token!")
    except Exception as e:
        logger.error(f"Token error: {e}")
        raise HTTPException(status_code=401, detail="Token error!")