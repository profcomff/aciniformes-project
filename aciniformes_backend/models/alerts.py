"""Классы хранения настроек нотификаций
"""
from datetime import datetime
from .base import BaseModel
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String


class Receiver(BaseModel):
    id_ = Column("id", Integer, primary_key=True)
    name = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=False)
    create_ts = Column(DateTime, default=datetime.utcnow)
    modify_ts = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Alert(BaseModel):
    id_ = Column("id", Integer, primary_key=True)
    data = Column(JSON, nullable=False)
    receiver = Column(Integer, ForeignKey("receiver.id"), nullable=False)
    filter = Column(String, nullable=False)
    create_ts = Column(DateTime, default=datetime.utcnow)
    modify_ts = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
