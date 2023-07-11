from functools import lru_cache

from pydantic import ConfigDict, HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BACKEND_URL: HttpUrl = "http://127.0.0.1:8000"
    BOT_URL: HttpUrl = "http://127.0.0.1:8001"
    model_config = ConfigDict(case_sensitive=True, env_file=".env", extra="ignore")


@lru_cache()
def get_settings():
    return Settings()
