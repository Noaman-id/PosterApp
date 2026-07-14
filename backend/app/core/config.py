from pathlib import Path
from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

load_dotenv(Path(__file__).resolve().parent.parent.parent.parent / ".env")

class Config(BaseSettings):
    app_name: str = "ScalableFastAPIProject"
    debug: bool = False
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = ""
    DB_PORT: str = ""
    DB_HOST: str = ""
    secret_key: str = ""

    @property
    def db_url(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

config = Config()
