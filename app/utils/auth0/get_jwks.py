import json
from urllib.request import urlopen

from core.settings import AUTH0_DOMAIN, logger


def get_jwks() -> dict:
    logger.info("Getting jwks from Auth0.")
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    response = urlopen(jwks_url)
    
    return json.loads(response.read())