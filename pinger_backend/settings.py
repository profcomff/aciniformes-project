from functools import lru_cache

from dotenv import load_dotenv
from pydantic import ConfigDict, PostgresDsn
from pydantic_settings import BaseSettings


load_dotenv(verbose=True)


class Settings(BaseSettings):
    DB_DSN: PostgresDsn
    model_config = ConfigDict(case_sensitive=True, env_file="../.env", extra="ignore")


@lru_cache()
def get_settings():
    return Settings()
