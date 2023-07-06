import time
from abc import ABC

import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aciniformes_backend.models import Fetcher, FetcherType, Receiver, Alert, Metric
from aciniformes_backend.routes.alert.alert import CreateSchema as AlertCreateSchema
from aciniformes_backend.routes.mectric import CreateSchema as MetricCreateSchema
from pinger_backend.service.session import dbsession

from .crud import CrudService
from .exceptions import AlreadyRunning, AlreadyStopped


class ApSchedulerService(ABC):
    scheduler = AsyncIOScheduler()
    backend_url = str

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
        fetchers = dbsession().query(Fetcher).all()
        self.scheduler.start()
        for fetcher in fetchers:
            self.add_fetcher(fetcher)
            await self._fetch_it(fetcher)

    def stop(self):
        if not self.scheduler.running:
            raise AlreadyStopped
        for job in self.scheduler.get_jobs():
            job.remove()
        self.scheduler.shutdown()

    def write_alert(self, metric_log: MetricCreateSchema, alert: AlertCreateSchema):
        receivers = dbsession().query(Receiver).all()
        session = dbsession()
        alert = Alert(**alert.dict(exclude_none=True))
        session.add(alert)
        session.commit()
        session.flush()
        for receiver in receivers:
            receiver.receiver_body['text'] = metric_log
            requests.request(method="POST", url=receiver.url, data=receiver['receiver_body'])

    @staticmethod
    def _parse_timedelta(fetcher: Fetcher):
        return fetcher.delay_ok, fetcher.delay_fail

    async def _fetch_it(self, fetcher: Fetcher):
        prev = time.time()
        res = None
        try:
            match fetcher.type_:
                case FetcherType.GET:
                    res = requests.request(method="GET", url=fetcher.address)
                case FetcherType.POST:
                    res = requests.request(method="POST", url=fetcher.address, data=fetcher.fetch_data)
                case FetcherType.PING:
                    res = requests.request(method="HEAD", url=fetcher.address)
        except:
            cur = time.time()
            timing = cur - prev
            metric = MetricCreateSchema(
                name=fetcher.address, ok=True if res and (200 <= res.status_code <= 300) else False, time_delta=timing
            )
            if metric.name not in [item.name for item in dbsession().query(Metric).all()]:
                self.crud_service.add_metric(metric)
            else:
                if metric.ok != dbsession().query(Metric).filter(Metric.name == metric.name).one_or_none().ok:
                    dbsession().query(Metric).filter(Metric.name == metric.name).delete()
                    self.crud_service.add_metric(metric)
            alert = AlertCreateSchema(data=metric, filter=500)
            if alert.data["name"] not in [item.data["name"] for item in dbsession().query(Alert).all()]:
                self.write_alert(metric, alert)
            self.scheduler.reschedule_job(
                f"{fetcher.address} {fetcher.create_ts}",
                seconds=fetcher.delay_fail,
                trigger="interval",
            )
            return
        cur = time.time()
        timing = cur - prev
        metric = MetricCreateSchema(
            name=fetcher.address, ok=True if res and (200 <= res.status_code <= 300) else False, time_delta=timing
        )
        if metric.name not in [item.name for item in dbsession().query(Metric).all()]:
            self.crud_service.add_metric(metric)
        else:
            if metric.ok != dbsession().query(Metric).filter(Metric.name == metric.name).one_or_none().ok:
                dbsession().query(Metric).filter(Metric.name == metric.name).delete()
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
