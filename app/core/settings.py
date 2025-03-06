from typing import List
from pydantic import computed_field
from pydantic_settings import BaseSettings
import pathlib

class Settings(BaseSettings):
    app_host: str
    app_port: int
    
    redis_host: str
    redis_port: int
    
    @computed_field
    @property
    def redis_url(self) -> str:
        return (f"redis://{self.redis_host}:{self.redis_port}")

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int
    
    @computed_field
    @property
    def database_url(self) -> str:
        return (f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@"
                f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}")
    
    cors_origins: List[str]
    
    class Config:
        env_file = str(pathlib.Path(__file__).resolve().parents[2] / ".env")
        

settings = Settings()
