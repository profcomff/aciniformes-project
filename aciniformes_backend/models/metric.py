"""Классы хранения метрик
"""

from datetime import datetime
from .base import BaseModel
from sqlalchemy import Integer, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class Metric(BaseModel):
    id_: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    metrics: Mapped[dict] = mapped_column(JSON, nullable=False)
    create_ts: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
