"""Классы хранения настроек автоматического мониторинга
"""
from datetime import datetime
from enum import Enum

import sqlalchemy
from sqlalchemy import JSON, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class FetcherType(str, Enum):
    GET = "get_ok"  # Пишет True, если GET запрос вернул статус 200..299
    POST = "post_ok"  # Пишет True, если POST запрос вернул статус 200..299
    PING = "ping_ok"  # Пишет True, если PING успешный


class Fetcher(BaseModel):
    id_: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type_: Mapped[FetcherType] = mapped_column(
        "type", sqlalchemy.Enum(FetcherType, native_enum=False), nullable=False
    )
    address: Mapped[str] = mapped_column(String, nullable=False)
    fetch_data: Mapped[str] = mapped_column(
        String
    )  # Данные, которые передаются в теле POST запроса
    metrics: Mapped[dict] = mapped_column(
        JSON, default={}, nullable=False
    )  # Статическая часть метрик
    metric_name: Mapped[str] = mapped_column(
        String, nullable=False
    )  # Название динамической части метрик
    delay_ok: Mapped[int] = mapped_column(
        Integer, default=300, nullable=False
    )  # Через сколько секунд повторить запрос, если предыдущий успешный
    delay_fail: Mapped[int] = mapped_column(
        Integer, default=30, nullable=False
    )  # Через сколько секунд повторить запрос, если предыдущий неуспешный
    create_ts: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    modify_ts: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
