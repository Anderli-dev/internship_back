from dotenv import load_dotenv
import os

load_dotenv()

def get_app_url():
    return f"http://{os.getenv("APP_HOST")}:{os.getenv("APP_PORT")}"