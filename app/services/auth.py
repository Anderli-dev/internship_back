from datetime import datetime, timedelta
from typing import Optional

from core.logger import logger
from core.settings import settings
from db.models import User
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.auth0.get_jwks import get_jwks
from utils.auth0.get_rsa_key import get_rsa_key
from utils.auth0.get_token_payload import get_token_payload
from utils.decorators.token_exception_check import token_exception_check
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
    
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, settings.jwt_algorithm)
    
    logger.info("Token creation success.")
    return encoded_jwt

class Auth:
    security = HTTPBearer()
    
    async def get_token_payload(self, credentials: HTTPAuthorizationCredentials = Security(security)):
        token = credentials.credentials
        
        try:
            return await self.get_auth0_jwt_token(token)
        except KeyError:
            return await self.get_jwt_token(token)
        
    @token_exception_check
    async def get_jwt_token(self, token: str):
        token_data = jwt.decode(token, settings.secret_key, settings.jwt_algorithm)
        return token_data
    
    @token_exception_check
    async def get_auth0_jwt_token(self, token: str):
        jwks = get_jwks()
        
        rsa_key = get_rsa_key(jwks, token)

        if not rsa_key:
            logger.error("Auth0 token invalid JWT Key.")
            raise HTTPException(status_code=401, detail="Invalid JWT Key")

        token_data = get_token_payload(token, rsa_key)
        
        return token_data
    