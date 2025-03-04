import json
from urllib.request import urlopen

import jwt
from core.settings import (ALGORITHMS, AUTH0_AUDIENCE, AUTH0_DOMAIN)
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

token_auth_sheme = HTTPBearer()

def get_jwks():
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    response = urlopen(jwks_url)
    return json.loads(response.read())

async def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(token_auth_sheme)):
    try:
        token = credentials.credentials
        
        header = jwt.get_unverified_header(token)
        jwks = get_jwks()

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

        if not rsa_key:
            raise HTTPException(status_code=401, detail="Invalid JWT Key")

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=AUTH0_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/"
        )
        
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