from .base import BaseModel
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Auth(BaseModel):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(String, nullable=False, doc="Hashed password")
