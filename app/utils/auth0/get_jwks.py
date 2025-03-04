import json
from urllib.request import urlopen

from core.settings import AUTH0_DOMAIN


def get_jwks():
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    response = urlopen(jwks_url)
    return json.loads(response.read())