import requests
from core.settings import settings
from core.logger import logger
from fastapi import HTTPException


async def get_management_token():
    headers = {'content-type': 'application/json'}
    data = {
        'client_id': settings.client_id,
        'client_secret': settings.client_secret,
        'audience': settings.auth0_domain,
        'grant_type': 'client_credentials'
    }
    response = requests.post(f"https://{settings.auth0_domain}/oauth/token", json=data, headers=headers)
    
    if response.status_code != 200:
        logger.info("Getting tokens from Auth0 error: failed to fetch token.")
        raise HTTPException(status_code=400, detail="Failed to fetch token!")

    tokens = response.json()
    logger.info("Getting tokens from Auth0 success.")
    return tokens["access_token"]