import asyncio
import json
from datetime import datetime, timedelta
from typing import Optional
from urllib.request import urlopen

import requests
from core.exceptions import Auth0Error, InvalidToken
from core.logger import logger
from core.settings import settings
from db.models import User
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt
from repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from utils.hash_password import verify_password

from db.schemas.UserSchema import UserSignIn


class AuthService:
    def __init__(self, db: AsyncSession):
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
        self.repo = UserRepository(db)

    async def authenticate_user(self, user_email: str, password: str) -> User:
        logger.info("User authentication.")
        user: User = await self.repo.get_user_by_email(user_email)
        
        if not user or not verify_password(password, user.password):
            logger.error("Incorrect username or password!")
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
    
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials) -> User:
        try:
            return await self.verify_auth0_jwt(credentials)
        except Exception:
            logger.info("User is not Auth0.")
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
        
        jwks = Auth0Service.get_jwks()
        
        rsa_key = Auth0Service.get_rsa_key(jwks, token)

        if not rsa_key:
            logger.error("Auth0 token invalid JWT Key.")
            raise InvalidToken

        payload = Auth0Service.get_token_payload(token, rsa_key)
        logger.info("Auth0 token verification success.")

        user: User = await self.repo.get_user_by_email(payload["user_email"])
        
        if not user:
            logger.error("User not found!")
            return None

        return user
    
    async def login_for_access_token(self, user_data: UserSignIn) -> dict:
        user = await self.authenticate_user(user_data.email, user_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = await self.create_access_token(data={"user_email": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    
class Auth0Service:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        
    async def add_user_if_not_exists(self, email: str) -> User:
        user = await self.repo.get_user_by_email(email)
        
        if not user:
            logger.info("Auth0 user dose not exist.")
            user = await self.repo.create({"email":email})
            logger.info("Auth0 user created.")
            return user
        
        return user
    
    @staticmethod
    def get_tokens(code: str) -> dict:
        # Getting tokes, not only access token but may be and id_token
        logger.info("Getting tokens from Auth0.")
        token_data = {
            "grant_type": "authorization_code",
            "client_id": settings.client_id,
            "client_secret": settings.client_secret,
            "code": code,
            "redirect_uri": f"http://{settings.auth0_app_host}:{settings.app_port}/auth/callback"
        }

        response = requests.post(f"https://{settings.auth0_domain}/oauth/token", json=token_data)
        
        if response.status_code != 200:
            logger.info("Getting tokens from Auth0 error: failed to fetch token.")
            raise Auth0Error(detail="Failed to fetch token!")

        tokens = response.json()
        logger.info("Getting tokens from Auth0 success.")
        return tokens

    @classmethod
    def get_email_from_token(self, token: str) -> str:
        logger.info("Getting email from Auth0 token.")
        jwks = self.get_jwks()
        
        rsa_key = self.get_rsa_key(jwks, token)

        if not rsa_key:
            logger.error("Auth0 invalid JWT Key when getting email.")
            raise Auth0Error(detail="Invalid JWT Key!")
        
        payload = self.get_token_payload(token, rsa_key)
        # Payload inclludes parameter "user_email" that consist email of user
        email = payload.get("user_email")

        if email is None:
            logger.error("Auth0 invalid token when getting email.")
            raise Auth0Error(detail="Invalid token!")
        
        return email
    
    @staticmethod
    def get_jwks() -> dict:
        logger.info("Getting jwks from Auth0.")
        jwks_url = f"https://{settings.auth0_domain}/.well-known/jwks.json"
        try:
            response = urlopen(jwks_url)
        except Exception:
            raise Auth0Error()
        
        return json.loads(response.read())
    
    @staticmethod
    def get_rsa_key(jwks: dict, token: str) -> dict:
        logger.info("Getting rsa_key from Auth0.")
        header = jwt.get_unverified_header(token)
        rsa_key = {}

        for key in jwks["keys"]:
            if key["kid"] == header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        
        return rsa_key
    
    @staticmethod
    def get_token_payload(token: str, rsa_key: dict) -> dict:
        logger.info("Getting token payload from Auth0.")
        payload = jwt.decode(token,
            rsa_key,
            algorithms=settings.auth0_algorithm,
            audience=settings.auth0_audience,
            issuer=f"https://{settings.auth0_domain}/")
        
        if payload is None:
            logger.error("Getting token payload from Auth0 error: invalid token.")
            raise Auth0Error(detail="Invalid Auth0 token!")
        
        logger.info("Getting token payload from Auth0 success.")
        return payload