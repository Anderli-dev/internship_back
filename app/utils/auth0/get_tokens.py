import requests
from core.settings import AUTH0_DOMAIN, CLIENT_ID, CLIENT_SECRET
from fastapi import HTTPException


async def get_tokens(code):
    token_data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": "http://localhost:8000/auth/callback"
    }

    response = requests.post(f"https://{AUTH0_DOMAIN}/oauth/token", json=token_data)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch token!")

    tokens = response.json()
    return tokens