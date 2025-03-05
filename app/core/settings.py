from pydantic_settings import BaseSettings
import pathlib

class Settings(BaseSettings):
    app_name: str = "MyApp"
    debug: bool = False
    
    app_host: str
    app_port: int
    
    redis_url: str
    database_url: str

    postgres_user: str
    postgres_password: str
    postgres_db: str

    class Config:
        env_file = str(pathlib.Path(__file__).resolve().parents[2] / ".env")
        

settings = Settings()
