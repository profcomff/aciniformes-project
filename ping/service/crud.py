from abc import ABC, abstractmethod

import httpx

from aciniformes_backend.models import Fetcher, Alert
from aciniformes_backend.routes.mectric import CreateSchema as MetricCreateSchema
from ping.settings import get_settings


class CrudServiceInterface(ABC):
    @abstractmethod
    async def get_fetchers(self) -> list[Fetcher]:
        raise NotImplementedError

    @abstractmethod
    async def add_metric(self, metric: MetricCreateSchema):
        raise NotImplementedError

    @abstractmethod
    async def get_alerts(self) -> list[Alert]:
        raise NotImplementedError


class CrudService(CrudServiceInterface):
    def __init__(self):
        self.backend_url: str = get_settings().BACKEND_URL

    async def get_fetchers(self) -> list[Fetcher]:
        return [Fetcher(**d) for d in httpx.get(f"{self.backend_url}/fetcher").json()]

    async def add_metric(self, metric: MetricCreateSchema):
        return httpx.post(f"{self.backend_url}/metric", data=metric.json())

    async def get_alerts(self) -> list[Alert]:
        return httpx.get(f"{self.backend_url}/alert").json()


class FakeCrudService(CrudServiceInterface):
    id_incr = 0
    fetcher_repo: dict[int, Fetcher] = dict()
    alert_repo: dict[int, Alert] = dict()
    metric_repo: dict[int, MetricCreateSchema] = dict()

    async def get_fetchers(self) -> list[Fetcher]:
        return list(self.fetcher_repo.values())

    async def add_metric(self, metric: MetricCreateSchema):
        self.metric_repo[self.id_incr] = metric
        self.id_incr += 1

    async def get_alerts(self) -> list[Alert]:
        return list(self.alert_repo.values())
