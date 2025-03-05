import jwt
from core.settings import logger
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from utils.auth0.get_jwks import get_jwks
from utils.auth0.get_rsa_key import get_rsa_key
from utils.auth0.get_token_payload import get_token_payload

token_auth_sheme = HTTPBearer()


async def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(token_auth_sheme)):
    logger.info("Auth0 token verification.")
    try:
        token = credentials.credentials
        
        jwks = get_jwks()
        
        rsa_key = get_rsa_key(jwks, token)

        if not rsa_key:
            logger.error("Auth0 token invalid JWT Key.")
            raise HTTPException(status_code=401, detail="Invalid JWT Key")

        payload = get_token_payload(token, rsa_key)
        
        data = payload.get("sub")
        if data is None:
            logger.error("Auth0 invalid token.")
            raise HTTPException(status_code=401, detail="Invalid token")
        
        logger.info("Auth0 token verification success.")
        return data

    except jwt.ExpiredSignatureError:
        logger.error("Auth0 token expired.")
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTClaimsError:
        logger.error("Auth0 token invalid claims.")
        raise HTTPException(status_code=401, detail="Invalid claims")
    except JWTError:
        logger.error("Auth0 invalid token.")
        raise HTTPException(status_code=401, detail="Invalid token")