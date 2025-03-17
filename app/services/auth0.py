from core.logger import logger
from db.models import User
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.auth0.get_jwks import get_jwks
from utils.auth0.get_rsa_key import get_rsa_key
from utils.auth0.get_token_payload import get_token_payload

security = HTTPBearer()

async def verify_auth0_jwt(db: AsyncSession, credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    logger.info("Auth0 token verification.")
    try:
        token = credentials.credentials
        jwks = get_jwks()
        
        rsa_key = get_rsa_key(jwks, token)

        if not rsa_key:
            logger.error("Auth0 token invalid JWT Key.")
            raise HTTPException(status_code=401, detail="Invalid JWT Key")

        payload = get_token_payload(token, rsa_key)
        logger.info("Auth0 token verification success.")

        user = await db.execute(select(User).filter(User.email == payload["user_email"]))
        user = user.scalars().first()
        
        if not user:
            logger.error("User not found!")
            raise HTTPException(status_code=404, detail="User not found!")

        return user
    
    except jwt.ExpiredSignatureError:
        logger.error("Auth0 token expired.")
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTClaimsError:
        logger.error("Auth0 token invalid claims.")
        raise HTTPException(status_code=401, detail="Invalid claims")
    except JWTError:
        logger.error("Auth0 invalid token.")
        raise HTTPException(status_code=401, detail="Invalid token")