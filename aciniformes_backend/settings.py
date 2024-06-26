from functools import lru_cache

from pydantic import ConfigDict, HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_DSN: PostgresDsn = 'postgresql://postgres@localhost:5432/postgres'

    CORS_ALLOW_ORIGINS: list[str] = ['*']
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ['*']
    CORS_ALLOW_HEADERS: list[str] = ['*']

    BACKEND_URL: HttpUrl = "http://127.0.0.1:8000"
    FETCHERS_UPDATE_DELAY_IN_SECONDS: int = 10
    model_config = ConfigDict(case_sensitive=True, env_file=".env", extra="ignore")


@lru_cache()
def get_settings():
    return Settings()
