import datetime
from functools import lru_cache

from passlib.context import CryptContext
from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    DB_DSN: PostgresDsn
    PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
    EXPIRY_TIMEDELTA: datetime.timedelta = datetime.timedelta(days=7)
    ADMIN_SECRET: dict[str, str] = {"admin": "42"}
    JWT_KEY = "42"
    ALGORITHM: str = "HS256"

    class Config:
        """Pydantic BaseSettings config"""

        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
