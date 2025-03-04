import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from utils.auth0.get_jwks import get_jwks
from utils.auth0.get_rsa_key import get_rsa_key
from utils.auth0.get_token_payload import get_token_payload

token_auth_sheme = HTTPBearer()


async def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(token_auth_sheme)):
    try:
        token = credentials.credentials
        
        jwks = get_jwks()
        
        rsa_key = await get_rsa_key(jwks, token)

        if not rsa_key:
            raise HTTPException(status_code=401, detail="Invalid JWT Key")

        payload = get_token_payload(token, rsa_key)
        
        data = payload.get("sub")
        if data is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTClaimsError:
        raise HTTPException(status_code=401, detail="Invalid claims")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")