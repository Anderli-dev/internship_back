import requests
from core.settings import AUTH0_DOMAIN, CLIENT_ID, CLIENT_SECRET, logger, AUTH0_AUDIENCE
from fastapi import HTTPException


async def get_management_token():
    headers = {'content-type': 'application/json'}
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'audience': AUTH0_AUDIENCE,
        'grant_type': 'client_credentials'
    }
    response = requests.post(f"https://{AUTH0_DOMAIN}/oauth/token", json=data, headers=headers)
    
    if response.status_code != 200:
        logger.info("Getting tokens from Auth0 error: failed to fetch token.")
        raise HTTPException(status_code=400, detail="Failed to fetch token!")

    tokens = response.json()
    logger.info("Getting tokens from Auth0 success.")
    return tokens["access_token"]