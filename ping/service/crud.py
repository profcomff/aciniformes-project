from abc import ABC, abstractmethod
from aciniformes_backend.models import Fetcher
from aciniformes_backend.routes.mectric import CreateSchema as MetricCreateSchema
from ping.settings import get_settings


class CrudServiceInterface(ABC):
    @abstractmethod
    async def get_fetchers(self) -> list[Fetcher]:
        raise NotImplementedError

    @abstractmethod
    async def add_metric(self, metric: MetricCreateSchema):
        raise NotImplementedError


class CrudService(CrudServiceInterface):
    def __init__(self):
        self.backend_url: str = get_settings().BACKEND_URL

    async def get_fetchers(self) -> list[Fetcher]:
        raise NotImplementedError

    async def add_metric(self, metric: MetricCreateSchema):
        raise NotImplementedError


class FakeCrudService(CrudServiceInterface):
    id_incr = 0
    fetcher_repo: dict[int, Fetcher] = dict()
    metric_repo: dict[int, MetricCreateSchema] = dict()

    async def get_fetchers(self) -> list[Fetcher]:
        return list(self.fetcher_repo.values())

    async def add_metric(self, metric: MetricCreateSchema):
        self.metric_repo[self.id_incr] = metric
