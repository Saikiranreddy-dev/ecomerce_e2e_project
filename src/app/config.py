from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Add your configuration variables here
    app_name: str = "My FastAPI App"
    debug: bool = True
    #database_url: str = "sqlite:///./test.db"
    #DB
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: int = 0
    DB_NAME: str = "ecomerce_e2e_project"
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"