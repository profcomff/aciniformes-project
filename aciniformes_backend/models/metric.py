"""Классы хранения метрик
"""

from datetime import datetime
from .base import BaseModel
from sqlalchemy import Column, Integer, JSON, DateTime


class Metric(BaseModel):
    id_ = Column("id", Integer, primary_key=True)
    metrics = Column(JSON, nullable=False)
    create_ts = Column(DateTime, default=datetime.utcnow)
