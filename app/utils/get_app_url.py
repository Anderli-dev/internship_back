import os

from dotenv import load_dotenv

load_dotenv()

def get_app_url():
    app_host = os.getenv("APP_HOST")
    app_port = os.getenv("APP_PORT")
    
    return f"http://{app_host}:{app_port}"