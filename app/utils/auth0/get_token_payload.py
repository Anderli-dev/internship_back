from core.settings import ALGORITHMS, AUTH0_AUDIENCE, AUTH0_DOMAIN
from fastapi import HTTPException
from jose import jwt


async def get_token_payload(token, rsa_key):
    try:
        payload = jwt.decode(token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=AUTH0_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/")
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except jwt.DecodeError:
        raise HTTPException(status_code=400, detail="Failed to decode token!")