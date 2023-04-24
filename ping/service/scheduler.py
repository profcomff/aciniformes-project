import time
from abc import ABC, abstractmethod

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler, BaseScheduler

from aciniformes_backend.models import Alert, Fetcher, FetcherType
from aciniformes_backend.routes.alert.alert import CreateSchema as AlertCreateSchema
from aciniformes_backend.routes.mectric import CreateSchema as MetricCreateSchema
from ping.settings import get_settings

from .crud import CrudServiceInterface
from .exceptions import AlreadyRunning

settings = get_settings()


class SchedulerServiceInterface(ABC):
    crud_service: CrudServiceInterface
    scheduler: BaseScheduler | dict

    @abstractmethod
    async def add_fetcher(self, fetcher: Fetcher):
        raise NotImplementedError

    @abstractmethod
    async def delete_fetcher(self, fetcher: Fetcher):
        raise NotImplementedError

    @abstractmethod
    async def get_jobs(self):
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
        return self.crud_service.get_alerts()


class FakeSchedulerService(SchedulerServiceInterface):
    scheduler = dict()

    def __init__(self, crud_service: CrudServiceInterface):
        self.crud_service = crud_service

    async def add_fetcher(self, fetcher: Fetcher):
        self.scheduler[fetcher.id_] = fetcher

    async def delete_fetcher(self, fetcher: Fetcher):
        del self.scheduler[fetcher.id_]

    async def get_jobs(self):
        return await self.crud_service.get_fetchers()

    async def start(self):
        if "started" in self.scheduler:
            raise AlreadyRunning
        self.scheduler["started"] = True

    async def stop(self):
        self.scheduler["started"] = False

    async def write_alert(self, metric_log: MetricCreateSchema, alert: Alert):
        httpx.post(f"{settings.BOT_URL}/alert", json=metric_log.json())


class ApSchedulerService(SchedulerServiceInterface):
    scheduler = AsyncIOScheduler()

    def __init__(self, crud_service: CrudServiceInterface):
        self.crud_service = crud_service

    async def add_fetcher(self, fetcher: Fetcher):
        self.scheduler.add_job(
            self._fetch_it,
            args=[fetcher],
            id=f"{fetcher.address} {fetcher.create_ts}",
            seconds=fetcher.delay_ok,
            trigger="interval",
        )

    async def delete_fetcher(self, fetcher: Fetcher):
        self.scheduler.remove_job(fetcher.name)

    async def get_jobs(self):
        return [j.id for j in self.scheduler.get_jobs()]

    async def start(self):
        if self.scheduler.running:
            self.scheduler.shutdown()
            raise AlreadyRunning
        fetchers = httpx.get(f"{settings.BACKEND_URL}/fetcher").json()
        self.scheduler.start()
        for fetcher in fetchers:
            fetcher = Fetcher(**fetcher)
            await self.add_fetcher(fetcher)
            await self._fetch_it(fetcher)

    async def stop(self):
        for job in self.scheduler.get_jobs():
            job.remove()
        self.scheduler.shutdown()

    async def write_alert(self, metric_log: MetricCreateSchema, alert: AlertCreateSchema):
        receivers = httpx.get(f"{settings.BACKEND_URL}/receiver").json()
        for receiver in receivers:
            receiver['receiver_body']['text'] = metric_log
            httpx.post(receiver['url'], data=receiver['receiver_body'])

    @staticmethod
    async def _parse_timedelta(fetcher: Fetcher):
        return fetcher.delay_ok, fetcher.delay_fail

    async def _fetch_it(self, fetcher: Fetcher):
        prev = time.time()
        res = None
        try:
            match fetcher.type_:
                case FetcherType.GET:
                    res = httpx.get(fetcher.address)
                case FetcherType.POST:
                    res = httpx.post(fetcher.address, data=fetcher.fetch_data)
                case FetcherType.PING:
                    res = httpx.head(fetcher.address)
        except:
            cur = time.time()
            timing = cur - prev
            metric = MetricCreateSchema(
                name=fetcher.address,
                ok=True if res and res.status_code == 200 else False,
                time_delta=timing
            )
            await self.crud_service.add_metric(metric)
            alert = AlertCreateSchema(data=metric, filter=500)
            self.scheduler.reschedule_job(
                f"{fetcher.address} {fetcher.create_ts}",
                seconds=fetcher.delay_fail,
                trigger="interval",
            )
            await self.write_alert(metric, alert)
            return
        cur = time.time()
        timing = cur - prev
        metric = MetricCreateSchema(
            name=fetcher.address,
            ok=True if res and res.status_code == 200 else False,
            time_delta=timing
        )
        await self.crud_service.add_metric(metric)
        if not metric.ok:
            alert = AlertCreateSchema(data=metric, filter=res.status_code)
            self.scheduler.reschedule_job(
                f"{fetcher.address} {fetcher.create_ts}",
                seconds=fetcher.delay_fail,
                trigger="interval",
            )
            await self.write_alert(metric, alert)
        else:
            self.scheduler.reschedule_job(
                f"{fetcher.address} {fetcher.create_ts}",
                seconds=fetcher.delay_ok,
                trigger="interval",
            )

