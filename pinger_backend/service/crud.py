from abc import ABC

from aciniformes_backend.models import Alert, Fetcher, Metric
from aciniformes_backend.routes.mectric import CreateSchema as MetricCreateSchema
from settings import get_settings

from .session import dbsession


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
