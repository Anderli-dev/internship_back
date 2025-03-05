import os

from core.settings import logger
from dotenv import load_dotenv

load_dotenv()

def get_app_url():
    logger.info("Getting app url.")
    app_host = os.getenv("APP_HOST")
    app_port = os.getenv("APP_PORT")
    
    logger.info("Getting app url success.")
    return f"http://{app_host}:{app_port}"