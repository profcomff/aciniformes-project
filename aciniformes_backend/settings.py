from functools import lru_cache
from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    DB_DSN: PostgresDsn
    TGBOT_TOKEN: str | None


@lru_cache()
def get_settings():
    return Settings()
