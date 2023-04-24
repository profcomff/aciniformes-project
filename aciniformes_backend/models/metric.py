"""Классы хранения метрик
"""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Metric(BaseModel):
    id_: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    name: Mapped[str] = mapped_column("name", String, nullable=False)
    ok: Mapped[bool] = mapped_column("ok", Boolean, nullable=False, default=True)
    time_delta: Mapped[float] = mapped_column(Float, default=datetime.utcnow)
