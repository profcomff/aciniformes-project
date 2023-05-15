import time
from abc import ABC, abstractmethod

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler, BaseScheduler

from aciniformes_backend.models import Alert, Fetcher, FetcherType
from aciniformes_backend.routes.alert.alert import CreateSchema as AlertCreateSchema
from aciniformes_backend.routes.mectric import CreateSchema as MetricCreateSchema
from pinger_backend.settings import get_settings

from .crud import CrudServiceInterface
from .exceptions import AlreadyRunning, AlreadyStopped, ConnectionFail

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

    def add_fetcher(self, fetcher: Fetcher):
        self.scheduler[fetcher.id_] = fetcher

    def delete_fetcher(self, fetcher: Fetcher):
        del self.scheduler[fetcher.id_]

    def get_jobs(self):
        return self.crud_service.get_fetchers()

    def start(self):
        if "started" in self.scheduler:
            raise AlreadyRunning
        self.scheduler["started"] = True

    def stop(self):
        if not self.scheduler["started"]:
            raise AlreadyStopped
        self.scheduler["started"] = False

    def write_alert(self, metric_log: MetricCreateSchema, alert: Alert):
        httpx.post(f"{settings.BOT_URL}/alert", json=metric_log.json())


class ApSchedulerService(SchedulerServiceInterface):
    scheduler = AsyncIOScheduler()

    def __init__(self, crud_service: CrudServiceInterface):
        self.crud_service = crud_service

    def add_fetcher(self, fetcher: Fetcher):
        self.scheduler.add_job(
            self._fetch_it,
            args=[fetcher],
            id=f"{fetcher.address} {fetcher.create_ts}",
            seconds=fetcher.delay_ok,
            trigger="interval",
        )

    def delete_fetcher(self, fetcher: Fetcher):
        self.scheduler.remove_job(f"{fetcher.address} {fetcher.create_ts}")

    def get_jobs(self):
        return [j.id for j in self.scheduler.get_jobs()]

    def start(self):
        if self.scheduler.running:
            raise AlreadyRunning
        fetchers = httpx.get(f"{settings.BACKEND_URL}/fetcher").json()
        self.scheduler.start()
        for fetcher in fetchers:
            fetcher = Fetcher(**fetcher)
            self.add_fetcher(fetcher)
            self._fetch_it(fetcher)

    def stop(self):
        if not self.scheduler.running:
            raise AlreadyStopped
        for job in self.scheduler.get_jobs():
            job.remove()
        self.scheduler.shutdown()

    def write_alert(self, metric_log: MetricCreateSchema, alert: AlertCreateSchema):
        receivers = httpx.get(f"{settings.BACKEND_URL}/receiver").json()
        for receiver in receivers:
            receiver['receiver_body']['text'] = metric_log
            httpx.post(receiver['url'], data=receiver['receiver_body'])

    @staticmethod
    def _parse_timedelta(fetcher: Fetcher):
        return fetcher.delay_ok, fetcher.delay_fail

    def _fetch_it(self, fetcher: Fetcher):
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
            self.crud_service.add_metric(metric)
            alert = AlertCreateSchema(data=metric, filter=500)
            self.scheduler.reschedule_job(
                f"{fetcher.address} {fetcher.create_ts}",
                seconds=fetcher.delay_fail,
                trigger="interval",
            )
            self.write_alert(metric, alert)
            return
        cur = time.time()
        timing = cur - prev
        metric = MetricCreateSchema(
            name=fetcher.address,
            ok=True if res and (200 <= res.status_code <= 300) else False,
            time_delta=timing
        )
        self.crud_service.add_metric(metric)
        if not metric.ok:
            alert = AlertCreateSchema(data=metric, filter=res.status_code)
            self.scheduler.reschedule_job(
                f"{fetcher.address} {fetcher.create_ts}",
                seconds=fetcher.delay_fail,
                trigger="interval",
            )
            self.write_alert(metric, alert)
        else:
            self.scheduler.reschedule_job(
                f"{fetcher.address} {fetcher.create_ts}",
                seconds=fetcher.delay_ok,
                trigger="interval",
            )
