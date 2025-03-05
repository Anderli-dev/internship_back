from core.settings import ALGORITHMS, AUTH0_AUDIENCE, AUTH0_DOMAIN, logger
from fastapi import HTTPException
from jose import jwt


async def get_token_payload(token, rsa_key):
    logger.info("Getting token payload from Auth0.")
    try:
        payload = jwt.decode(token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=AUTH0_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/")
        if payload is None:
            logger.error("Getting token payload from Auth0 error: invalid token.")
            raise HTTPException(status_code=401, detail="Invalid token")
        logger.info("Getting token payload from Auth0 success.")
        return payload
    except jwt.DecodeError:
        logger.error("Getting token payload from Auth0 error: failed to decode token.")
        raise HTTPException(status_code=400, detail="Failed to decode token!")