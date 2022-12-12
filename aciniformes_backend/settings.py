from pydantic import BaseSettings


class Settings(BaseSettings):
    TGBOT_TOKEN: str | None
