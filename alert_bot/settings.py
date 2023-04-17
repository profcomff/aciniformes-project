from functools import lru_cache

from pydantic import BaseSettings, HttpUrl


class Settings(BaseSettings):
    BOT_TOKEN: str
    PING_URL: HttpUrl = "http://127.0.0.1:8001"
    BACKEND_URL: HttpUrl = "http://127.0.0.1:8000"

    class Config:
        """Pydantic BaseSettings config"""

        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
