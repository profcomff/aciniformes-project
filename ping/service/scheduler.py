from abc import ABC, abstractmethod
from aciniformes_backend.models import Fetcher, FetcherType, Alert
from aciniformes_backend.routes.mectric import CreateSchema as MetricCreateSchema
from .crud import CrudServiceInterface
from apscheduler.schedulers.asyncio import AsyncIOScheduler, BaseScheduler
import httpx
from datetime import datetime
import time


class SchedulerServiceInterface(ABC):
    crud_service: CrudServiceInterface
    scheduler: BaseScheduler | None

    @abstractmethod
    async def add_fetcher(self, fetcher: Fetcher):
        raise NotImplementedError

    @abstractmethod
    async def delete_fetcher(self, fetcher: Fetcher):
        raise NotImplementedError

    @abstractmethod
    async def start(self):
        raise NotImplementedError

    @abstractmethod
    async def stop(self):
        raise NotImplementedError

    @abstractmethod
    async def write_alert(self, metric_log: MetricCreateSchema, alert: Alert):
        raise NotImplementedError

    async def _add_metric(self, metric: MetricCreateSchema):
        await self.crud_service.add_metric(metric)

    @property
    def alerts(self):
        return await self.crud_service.get_alerts()


class FakeSchedulerService(SchedulerServiceInterface):
    def __init__(self, crud_service: CrudServiceInterface):
        self.scheduler = None
        self.container = crud_service

    async def add_fetcher(self, fetcher: Fetcher):
        pass

    async def delete_fetcher(self, fetcher: Fetcher):
        self.scheduler.remove_job(fetcher.name)

    async def start(self):
        pass

    async def stop(self):
        pass

    async def write_alert(self, metric_log: MetricCreateSchema, alert: Alert):
        raise NotImplementedError


class ApSchedulerService(SchedulerServiceInterface):
    def __init__(self, crud_service: CrudServiceInterface):
        self.scheduler = AsyncIOScheduler()
        self.crud_service = crud_service

    async def add_fetcher(self, fetcher: Fetcher):
        f = await self._fetch_it(fetcher)
        self.scheduler.add_job(
            f,
            name=f"{fetcher.name}",
            next_run_time=fetcher.delay_ok,
            trigger="interval",
        )

    async def delete_fetcher(self, fetcher: Fetcher):
        self.scheduler.remove_job(fetcher.name)

    async def start(self):
        self.scheduler.start()

    async def stop(self):
        self.scheduler.shutdown()

    async def write_alert(self, metric_log: MetricCreateSchema, alert: Alert):
        raise NotImplementedError

    @staticmethod
    async def _parse_timedelta(fetcher: Fetcher):
        return fetcher.delay_ok, fetcher.delay_fail

    async def _fetch_it(self, fetcher: Fetcher):
        prev = time.time()
        res = None
        match fetcher.type_:
            case FetcherType.GET:
                res = httpx.get(fetcher.address)
            case FetcherType.POST:
                res = httpx.post(fetcher.address, data=fetcher.fetch_data)
            case FetcherType.PING:
                res = httpx.get(fetcher.address)
        cur = time.time()
        timing = cur - prev
        metric = MetricCreateSchema(
            metrics={
                "status": res.status_code,
                "dt_created": datetime.utcnow(),
                "timing": timing,
            }
        )
        for alert in self.alerts:
            if alert.filter == str(res.status_code):
                await self.write_alert(metric, alert)
        await self.crud_service.add_metric(metric)