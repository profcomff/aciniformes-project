from abc import ABC, abstractmethod

from aciniformes_backend.models import Alert, Fetcher, Metric
from aciniformes_backend.routes.mectric import CreateSchema as MetricCreateSchema
from pinger_backend.service.session import dbsession
from pinger_backend.settings import get_settings


class CrudServiceInterface(ABC):
    @abstractmethod
    def get_fetchers(self) -> list[Fetcher]:
        raise NotImplementedError

    @abstractmethod
    def add_metric(self, metric: MetricCreateSchema):
        raise NotImplementedError

    @abstractmethod
    def get_alerts(self) -> list[Alert]:
        raise NotImplementedError


class CrudService(CrudServiceInterface):
    backend_url: str

    def __init__(self):
        self.backend_url = get_settings().BACKEND_URL

    def get_fetchers(self) -> list[Fetcher]:
        return [Fetcher(**d) for d in dbsession().query(Fetcher).all()]

    def add_metric(self, metric: MetricCreateSchema):
        metric = Metric(**metric.dict(exclude_none=True))
        dbsession().add(metric)
        dbsession().commit()
        dbsession().flush()
        return metric

    def get_alerts(self) -> list[Alert]:
        return [Alert(**d) for d in dbsession().query(Alert).all()]


class FakeCrudService(CrudServiceInterface):
    fetcher_repo: dict[int, Fetcher] = {
        0: Fetcher(
            **{
                "type_": "get_ok",
                "address": "https://www.python.org",
                "fetch_data": None,
                "delay_ok": 30,
                "delay_fail": 40,
            }
        )
    }
    alert_repo: dict[int, Alert] = dict()
    metric_repo: dict[int, MetricCreateSchema] = dict()

    def get_fetchers(self) -> list[Fetcher]:
        return list(self.fetcher_repo.values())

    def add_metric(self, metric: MetricCreateSchema):
        self.metric_repo[self.id_incr] = metric
        self.id_incr += 1

    def get_alerts(self) -> list[Alert]:
        return list(self.alert_repo.values())
