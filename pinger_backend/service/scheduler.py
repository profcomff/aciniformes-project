import time
from abc import ABC
from contextlib import asynccontextmanager
from typing import AsyncIterator

import ping3
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aciniformes_backend.models import Alert, Fetcher, FetcherType, Receiver
from aciniformes_backend.routes.alert.alert import CreateSchema as AlertCreateSchema
from aciniformes_backend.routes.mectric import CreateSchema as MetricCreateSchema
from pinger_backend.exceptions import AlreadyRunning, AlreadyStopped
from settings import get_settings

from .crud import CrudService
from .session import dbsession


class ApSchedulerService(ABC):
    scheduler = AsyncIOScheduler()
    settings = get_settings()
    backend_url = str
    fetchers: list

    def __init__(self, crud_service: CrudService):
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

    async def start(self):
        if self.scheduler.running:
            raise AlreadyRunning
        self.scheduler.add_job(
            self._fetcher_update_job,
            id="check_fetchers",
            seconds=self.settings.FETCHERS_UPDATE_DELAY_IN_SECONDS,
            trigger="interval",
        )
        self.fetchers = dbsession().query(Fetcher).all()
        self.scheduler.start()
        for fetcher in self.fetchers:
            self.add_fetcher(fetcher)
            await self._fetch_it(fetcher)

    def stop(self):
        if not self.scheduler.running:
            raise AlreadyStopped
        for job in self.scheduler.get_jobs():
            job.remove()
        self.scheduler.shutdown()

    def write_alert(self, alert: AlertCreateSchema):
        receivers = dbsession().query(Receiver).all()
        session = dbsession()
        alert = Alert(**alert.model_dump(exclude_none=True))
        session.add(alert)
        session.flush()
        for receiver in receivers:
            requests.request(method=receiver.method, url=receiver.url, data=receiver.receiver_body)

    @staticmethod
    def _parse_timedelta(fetcher: Fetcher) -> tuple[int, int]:
        return fetcher.delay_ok, fetcher.delay_fail

    @asynccontextmanager
    async def __update_fetchers(self) -> AsyncIterator[None]:
        jobs = [job.id for job in self.scheduler.get_jobs()]
        old_fetchers = self.fetchers
        new_fetchers = dbsession().query(Fetcher).all()

        # Проверка на удаление фетчера
        for fetcher in old_fetchers:
            if (fetcher.address not in [ftch.address for ftch in new_fetchers]) and (
                f"{fetcher.address} {fetcher.create_ts}" in jobs
            ):
                self.scheduler.remove_job(job_id=f"{fetcher.address} {fetcher.create_ts}")

        jobs = [job.id for job in self.scheduler.get_jobs()]
        # Проверка на добавление нового фетчера
        for fetcher in new_fetchers:
            if (f"{fetcher.address} {fetcher.create_ts}" not in jobs) and (
                fetcher.address not in [ftch.address for ftch in old_fetchers]
            ):
                self.add_fetcher(fetcher)
                self.fetchers.append(fetcher)
        yield
        self.scheduler.reschedule_job(
            "check_fetchers", seconds=self.settings.FETCHERS_UPDATE_DELAY_IN_SECONDS, trigger="interval"
        )

    async def _fetcher_update_job(self) -> None:
        async with self.__update_fetchers():
            pass

    @staticmethod
    def create_metric(prev: float, fetcher: Fetcher, res: requests.Response) -> MetricCreateSchema:
        cur = time.time()
        timing = cur - prev
        if fetcher.type_ != FetcherType.PING:
            return MetricCreateSchema(
                name=fetcher.address,
                ok=True if res and (200 <= res.status_code <= 300) else False,
                time_delta=timing,
            )
        return MetricCreateSchema(
            name=fetcher.address,
            ok=res is not False and res is not None,
            time_delta=timing,
        )

    def _reschedule_job(self, fetcher: Fetcher, ok: bool):
        self.scheduler.reschedule_job(
            f"{fetcher.address} {fetcher.create_ts}",
            seconds=fetcher.delay_ok if ok else fetcher.delay_fail,
            trigger="interval",
        )

    def _process_fail(self, fetcher: Fetcher, metric: MetricCreateSchema, res: requests.Response | None) -> None:
        if fetcher.type_ != FetcherType.PING:
            alert = AlertCreateSchema(data=metric.model_dump(), filter="500" if res is None else str(res.status_code))
        else:
            _filter = "Service Unavailable" if res is False else "Timeout Error" if res is None else "Unknown Error"
            alert = AlertCreateSchema(data=metric.model_dump(), filter=_filter)
        self.write_alert(alert)
        self._reschedule_job(fetcher, False)

    async def _fetch_it(self, fetcher: Fetcher):
        prev = time.time()
        res = None
        try:
            match fetcher.type_:
                case FetcherType.GET:
                    res = requests.get(url=fetcher.address)
                case FetcherType.POST:
                    res = requests.post(url=fetcher.address, data=fetcher.fetch_data)
                case FetcherType.PING:
                    res = ping3.ping(fetcher.address)
        except Exception:
            metric = ApSchedulerService.create_metric(prev, fetcher, res)
            self.crud_service.add_metric(metric)
            self._process_fail(fetcher, metric, None)
        else:
            metric = ApSchedulerService.create_metric(prev, fetcher, res)
            self.crud_service.add_metric(metric)
            if not metric.ok:
                self._process_fail(fetcher, metric, res)
            else:
                self._reschedule_job(fetcher, True)
