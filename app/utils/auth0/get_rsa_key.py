from core.logger import logger
from jose import jwt


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