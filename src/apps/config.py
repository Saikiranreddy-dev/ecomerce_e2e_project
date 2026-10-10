from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Add your configuration variables here
    app_name: str = "My FastAPI App"
    debug: bool = True
    #database_url: str = "sqlite:///./test.db"
    #DB
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: int
    DB_NAME: str = "ecomerce_e2e_project"
    SECRET_KEY: str
    ENCODING: str = "utf-8"
    ALGORITHM: str = "HS256"
    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent / ".env"
        env_file_encoding = "utf-8"


settings = Settings()