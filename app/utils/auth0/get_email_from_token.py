from core.logger import logger
from fastapi import HTTPException
from utils.auth0.get_jwks import get_jwks
from utils.auth0.get_rsa_key import get_rsa_key
from utils.auth0.get_token_payload import get_token_payload


def get_email_from_token(token: str) -> str:
    logger.info("Getting email from Auth0 token.")
    jwks = get_jwks()
    
    rsa_key = get_rsa_key(jwks, token)

    if not rsa_key:
        logger.error("Auth0 invalid JWT Key when getting email.")
        raise HTTPException(status_code=401, detail="Invalid JWT Key")
    
    payload = get_token_payload(token, rsa_key)
    # Payload inclludes parameter "user_email" that consist email of user
    email = payload.get("user_email")

    if email is None:
        logger.error("Auth0 invalid token when getting email.")
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return email