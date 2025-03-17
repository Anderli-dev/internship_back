from core.logger import logger
from core.settings import settings
from fastapi import HTTPException
from jose import jwt
from jose import exceptions


def get_token_payload(token: str, rsa_key: dict) -> dict:
    logger.info("Getting token payload from Auth0.")
    try:
        payload = jwt.decode(token,
            rsa_key,
            algorithms="RS256",
            audience=settings.auth0_audience,
            issuer=f"https://{settings.auth0_domain}/")
        if payload is None:
            logger.error("Getting token payload from Auth0 error: invalid token.")
            raise HTTPException(status_code=401, detail="Invalid token")
        logger.info("Getting token payload from Auth0 success.")
        return payload
    except exceptions.JWTError:
        logger.error("Getting token payload from Auth0 error: failed to decode token.")
        raise HTTPException(status_code=400, detail="Failed to decode token!")