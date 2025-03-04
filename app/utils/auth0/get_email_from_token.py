from fastapi import HTTPException
from utils.auth0.get_jwks import get_jwks
from utils.auth0.get_rsa_key import get_rsa_key
from utils.auth0.get_token_payload import get_token_payload


async def get_email_from_token(token):
    jwks = get_jwks()
    
    rsa_key = await get_rsa_key(jwks, token)

    if not rsa_key:
        raise HTTPException(status_code=401, detail="Invalid JWT Key")
    
    payload = await get_token_payload(token, rsa_key)
    email = payload.get("https://fast-api.example.com/email")
    
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return email