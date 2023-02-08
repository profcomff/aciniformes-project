from pydantic import BaseSettings, HttpUrl
from functools import lru_cache


class Settings(BaseSettings):
    BOT_TOKEN: str

    class Config:
        """Pydantic BaseSettings config"""

        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
