"""Классы хранения настроек автоматического мониторинга
"""
from datetime import datetime
from enum import Enum

from .base import JSON, BaseModel, Column, DateTime, Enum, Integer, String


class FetcherType(str, Enum):
    GET = 'get_ok'  # Пишет True, если GET запрос вернул статус 200..299
    POST = 'post_ok'  # Пишет True, если POST запрос вернул статус 200..299
    PING = 'ping_ok'  # Пишет True, если PING успешный


class Fetcher(BaseModel):
    id_ = Column('id', Integer, primary_key=True)
    name = Column(String, nullable=False)
    type_ = Column('type', Enum(FetcherType, native_enum=False), nullable=False)
    address = Column(String, nullable=False)
    fetch_data = Column(String)  # Данные, которые передаются в теле POST запроса
    matrics = Column(JSON, default={}, nullable=False)  # Статическая часть метрик
    matric_name = Column(String, nullable=False)  # Название динамической части метрик
    delay_ok = Column(Integer, default=300, nullable=False)  # Через сколько секунд повторить запрос, если предыдущий успешный
    delay_fail = Column(Integer, default=30, nullable=False)  # Через сколько секунд повторить запрос, если предыдущий неуспешный
    create_ts = Column(DateTime, default=datetime.utcnow)
    modify_ts = Column(DateTime, default=datetime.utcnow, on_update=datetime.utcnow)
