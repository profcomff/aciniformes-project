"""Классы хранения настроек нотификаций
"""
from datetime import datetime
from .base import BaseModel
from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Receiver(BaseModel):
    id_: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    chat_id: Mapped[int] = mapped_column(Integer, nullable=False)
    create_ts: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    modify_ts: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Alert(BaseModel):
    id_: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    data = mapped_column(JSON, nullable=False)
    receiver: Mapped[int] = mapped_column(Integer, ForeignKey("receiver.id", ondelete='CASCADE'), nullable=False)
    filter = mapped_column(String, nullable=False)
    create_ts = mapped_column(DateTime, default=datetime.utcnow)
    modify_ts = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
