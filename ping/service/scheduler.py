from abc import ABC, abstractmethod
from aciniformes_backend.models import Fetcher
from aciniformes_backend.routes.mectric import CreateSchema as MetricCreateSchema
from .crud import CrudServiceInterface
from apscheduler.schedulers.asyncio import AsyncIOScheduler, BaseScheduler


class SchedulerServiceInterface(ABC):
    crud_service: CrudServiceInterface
    scheduler: BaseScheduler | None

    @abstractmethod
    async def add_fetcher(self, fetcher: Fetcher):
        raise NotImplementedError

    @abstractmethod
    async def delete_fetcher(self):
        raise NotImplementedError

    @abstractmethod
    async def start(self):
        raise NotImplementedError

    @abstractmethod
    async def stop(self):
        raise NotImplementedError

    async def _add_metric(self, metric: MetricCreateSchema):
        await self.crud_service.add_metric(metric)


class FakeSchedulerService(SchedulerServiceInterface):
    def __init__(self, crud_service: CrudServiceInterface):
        self.scheduler = None
        self.crud_service = crud_service

    async def add_fetcher(self, fetcher: Fetcher):
        pass

    async def delete_fetcher(self):
        pass

    async def start(self):
        pass

    async def stop(self):
        pass


class ApSchedulerService(SchedulerServiceInterface):
    def __init__(self, crud_service: CrudServiceInterface):
        self.scheduler = AsyncIOScheduler()
        self.crud_service = crud_service

    async def add_fetcher(self, fetcher: Fetcher):
        self.scheduler.add_job(self.make_func(fetcher))

    async def delete_fetcher(self):
        pass

    async def start(self):
        pass

    async def stop(self):
        pass

    async def make_func(self, fetcher: Fetcher):
        pass
