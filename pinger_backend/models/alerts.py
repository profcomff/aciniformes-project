"""Классы хранения настроек нотификаций
"""
from datetime import datetime
from enum import Enum

from sqlalchemy import JSON, DateTime
from sqlalchemy import Enum as DbEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Method(str, Enum):
    POST: str = "post"
    GET: str = "get"


class Receiver(BaseModel):
    id_: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    method: Mapped[Method] = mapped_column(DbEnum(Method, native_enum=False), nullable=False)
    receiver_body: Mapped[dict] = mapped_column(JSON, nullable=False)
    create_ts: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Alert(BaseModel):
    id_: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    data = mapped_column(JSON, nullable=False)
    filter = mapped_column(String, nullable=False)
    create_ts = mapped_column(DateTime, default=datetime.utcnow)
