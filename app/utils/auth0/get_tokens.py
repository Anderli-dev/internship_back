import requests
from core.settings import (APP_URL, AUTH0_DOMAIN, CLIENT_ID, CLIENT_SECRET,
                           logger)
from fastapi import HTTPException


async def get_tokens(code):
    logger.info("Getting tokens from Auth0.")
    token_data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": f"{APP_URL}/auth/callback"
    }

    response = requests.post(f"https://{AUTH0_DOMAIN}/oauth/token", json=token_data)
    
    if response.status_code != 200:
        logger.info("Getting tokens from Auth0 error: failed to fetch token.")
        raise HTTPException(status_code=400, detail="Failed to fetch token!")

    tokens = response.json()
    logger.info("Getting tokens from Auth0 success.")
    return tokens