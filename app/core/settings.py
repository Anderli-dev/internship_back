import logging
import os
import sys
from dotenv import load_dotenv

load_dotenv()

HOST: str = "0.0.0.0"
PORT: int = 8000

DATABASE_URL: str = os.getenv("DATABASE_URL")
REDIS_URL: str = os.getenv("REDIS_URL")
SECRET_KEY: str = os.getenv("SECRET_KEY")

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.ERROR)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
