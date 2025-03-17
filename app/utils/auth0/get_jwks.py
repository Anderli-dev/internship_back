import json
from urllib.request import urlopen

from core.settings import settings
from core.logger import logger


def get_jwks() -> dict:
    logger.info("Getting jwks from Auth0.")
    jwks_url = f"https://{settings.auth0_domain}/.well-known/jwks.json"
    response = urlopen(jwks_url)
    
    return json.loads(response.read())