import logging
import os
import sys
from dotenv import load_dotenv

from utils.get_app_url import get_app_url

load_dotenv()

APP_URL: str = get_app_url()

HOST: str = "0.0.0.0"
PORT: int = 8000

DATABASE_URL: str = os.getenv("DATABASE_URL")
REDIS_URL: str = os.getenv("REDIS_URL")
    
SECRET_KEY: str = os.getenv("SECRET_KEY")

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
ALGORITHMS = ["RS256"]

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.ERROR)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
