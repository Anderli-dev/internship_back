import os
from dotenv import load_dotenv

load_dotenv()

HOST: str = "0.0.0.0"
PORT: int = 8000

DATABASE_URL: str = os.getenv("DATABASE_URL")
REDIS_URL: str = os.getenv("REDIS_URL")
