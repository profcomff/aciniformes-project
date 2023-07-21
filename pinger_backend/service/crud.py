import os
import sys
from abc import ABC


sys.path.append(os.path.realpath('..'))

from models import Alert, Fetcher, Metric
from routes.mectric import CreateSchema as MetricCreateSchema

from .session import dbsession
from .settings import get_settings


class CrudService(ABC):
    backend_url: str

    def __init__(self):
        self.backend_url = get_settings().BACKEND_URL

    def get_fetchers(self) -> list[Fetcher]:
        return [Fetcher(**d) for d in dbsession().query(Fetcher).all()]

    def add_metric(self, metric: MetricCreateSchema):
        session = dbsession()
        metric = Metric(**metric.model_dump(exclude_none=True))
        session.add(metric)
        session.commit()
        session.flush()
        return metric

    def get_alerts(self) -> list[Alert]:
        return [Alert(**d) for d in dbsession().query(Alert).all()]
