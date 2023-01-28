"""Классы хранения настроек нотификаций
"""
from datetime import datetime

from .base import JSON, BaseModel, Column, DateTime, ForeignKey, Integer, String


class Reciever(BaseModel):
    id_ = Column('id', Integer, primary_key=True)
    name = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=False)
    create_ts = Column(DateTime, default=datetime.utcnow)
    modify_ts = Column(DateTime, default=datetime.utcnow)  #, on_update=datetime.utcnow)


class Alert(BaseModel):
    id_ = Column('id', Integer, primary_key=True)
    data = Column(JSON, nullable=False)
    reciever_id = Column(Integer, ForeignKey('reciever.id'), nullable=False)
    filter_ = Column('filter', String, nullable=False)
    create_ts = Column(DateTime, default=datetime.utcnow)
    modify_ts = Column(DateTime, default=datetime.utcnow)  #, on_update=datetime.utcnow)
