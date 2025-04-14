import asyncio
from datetime import datetime, timedelta
from typing import Optional

from core.exceptions import InvalidToken
from utils.auth0.get_jwks import get_jwks
from utils.auth0.get_rsa_key import get_rsa_key
from utils.auth0.get_token_payload import get_token_payload
from core.logger import logger
from core.settings import settings
from db.models import User
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from utils.hash_password import verify_password

from repositories.auth_repository import AuthRepository
from db.models import User

class AuthService:
    def __init__(self, db: AsyncSession):
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
        self.repo = AuthRepository(db)

    async def authenticate_user(self, user_email: str, password: str) -> User:
        logger.info("User authentication.")
        user: User = await self.repo.get_user_by_email(user_email)
        
        if not user or not verify_password(password, user.password):
            return None
        
        logger.info("User authentication success.")
        return user

    async def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        logger.info("Creating token.")
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta or timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        
        loop = asyncio.get_running_loop()
        encoded_jwt = await loop.run_in_executor(None, jwt.encode, to_encode, settings.secret_key, settings.jwt_algorithm)
        
        logger.info("Token creation success.")
        return encoded_jwt
    
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials):
        try:
            return await self.verify_auth0_jwt(credentials)
        except Exception:
            return await self.verify_jwt(credentials)

    async def verify_jwt(self, credentials: HTTPAuthorizationCredentials) -> User:
        logger.debug("Getting user by token")
        
        token = credentials.credentials
        
        loop = asyncio.get_running_loop()
        decoded_jwt = await loop.run_in_executor(None, jwt.decode, token, settings.secret_key, settings.jwt_algorithm)
        
        user_email = decoded_jwt.get("user_email")
        if user_email is None:
            logger.error("Invalid token!")
            raise InvalidToken
        
        user: User = await self.repo.get_user_by_email(user_email)
        
        if not user:
            logger.error("User not found!")
            return None
        
        return user

    async def verify_auth0_jwt(self, credentials: HTTPAuthorizationCredentials) -> dict:
        logger.info("Auth0 token verification.")
        token = credentials.credentials
        
        jwks = get_jwks()
        
        rsa_key = get_rsa_key(jwks, token)

        if not rsa_key:
            logger.error("Auth0 token invalid JWT Key.")
            raise InvalidToken

        payload = get_token_payload(token, rsa_key)
        logger.info("Auth0 token verification success.")

        user: User = await self.repo.get_user_by_email(payload["user_email"])
        
        if not user:
            logger.error("User not found!")
            return None

        return user