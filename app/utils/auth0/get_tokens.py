import requests
from core.logger import logger
from core.settings import settings
from fastapi import HTTPException


def get_tokens(code: str) -> dict:
    # Getting tokes, not only access token but may be and id_token
    logger.info("Getting tokens from Auth0.")
    token_data = {
        "grant_type": "authorization_code",
        "client_id": settings.client_id,
        "client_secret": settings.client_secret,
        "code": code,
        "redirect_uri": f"http://{settings.auth0_app_host}:{settings.app_port}/auth/callback"
    }

    response = requests.post(f"https://{settings.auth0_domain}/oauth/token", json=token_data)
    
    if response.status_code != 200:
        logger.info("Getting tokens from Auth0 error: failed to fetch token.")
        raise HTTPException(status_code=400, detail="Failed to fetch token!")

    tokens = response.json()
    logger.info("Getting tokens from Auth0 success.")
    return tokens