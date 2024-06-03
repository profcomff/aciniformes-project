import logging
import string
import time

import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aciniformes_backend.exceptions import AlreadyRunning, AlreadyStopped
from aciniformes_backend.models import Alert, Fetcher, FetcherType, Metric, Receiver
from aciniformes_backend.settings import get_settings

from .ping import ping
from .session import session_factory


logger = logging.getLogger(__name__)


class ApSchedulerService:
    scheduler = AsyncIOScheduler()
    settings = get_settings()
    fetchers: list[Fetcher]

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
        logger.info("Starting scheduler service")
        if self.scheduler.running:
            raise AlreadyRunning
        self.scheduler.add_job(
            self.update_fetchers,
            id="check_fetchers",
            seconds=self.settings.FETCHERS_UPDATE_DELAY_IN_SECONDS,
            trigger="interval",
        )
        with session_factory() as session:
            self.fetchers = session.query(Fetcher).all()
        self.scheduler.start()
        for fetcher in self.fetchers:
            self.add_fetcher(fetcher)
            await self._fetch_it(fetcher)

    def stop(self):
        logger.info("Stopping scheduler service")
        if not self.scheduler.running:
            raise AlreadyStopped
        for job in self.scheduler.get_jobs():
            job.remove()
        self.scheduler.shutdown()

    async def write_alert(self, alert: Alert):
        with session_factory() as session:
            receivers: list[Receiver] = session.query(Receiver).all()
            session.add(alert)
            for receiver in receivers:
                # Заполняем тело письма, если в нем есть плейсхолдеры
                message_body = receiver.receiver_body
                for key, value in message_body.items():
                    if not isinstance(value, str):
                        continue
                    placeholders = set(tup[1] for tup in string.Formatter().parse(value) if tup[1] is not None)
                    placeholder_values = {}
                    for i in placeholders:
                        placeholder_values[i] = dict(alert.data).get(i)
                    message_body[key] = value.format(**placeholder_values)

                # Отправляем сообщение
                async with aiohttp.ClientSession() as s:
                    async with s.request(method=receiver.method, url=receiver.url, data=message_body):
                        pass
            session.commit()

    @staticmethod
    def _parse_timedelta(fetcher: Fetcher) -> tuple[int, int]:
        return fetcher.delay_ok, fetcher.delay_fail

    async def update_fetchers(self):
        jobs = [job.id for job in self.scheduler.get_jobs()]
        old_fetchers = self.fetchers
        with session_factory() as session:
            new_fetchers = session.query(Fetcher).all()

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

        self.scheduler.reschedule_job(
            "check_fetchers", seconds=self.settings.FETCHERS_UPDATE_DELAY_IN_SECONDS, trigger="interval"
        )

    @staticmethod
    def create_metric(prev: float, fetcher: Fetcher, res: aiohttp.ClientResponse) -> Metric:
        is_ok = {
            FetcherType.GET: lambda: res and (200 <= res.status <= 300),
            FetcherType.POST: lambda: res and (200 <= res.status <= 300),
            FetcherType.PING: lambda: res is not False and res is not None,
        }[fetcher.type_]()
        return Metric(name=fetcher.address, ok=is_ok, time_delta=time.time() - prev)

    async def process_fail(self, fetcher: Fetcher, metric: Metric, res: aiohttp.ClientResponse | None | float) -> None:
        logger.info("Fetcher %s failed", fetcher.address)
        if fetcher.type_ != FetcherType.PING:
            alert = Alert(data=metric.as_dict(), filter=res.status if isinstance(res, aiohttp.ClientResponse) else "500")
        else:
            _filter = "Service Unavailable" if res is False else "Timeout Error" if res is None else "Unknown Error"
            alert = Alert(data=metric.as_dict(), filter=_filter)
        await self.write_alert(alert)

    async def _fetch_it(self, fetcher: Fetcher):
        prev = time.time()
        res = None
        try:
            match fetcher.type_:
                case FetcherType.GET:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url=fetcher.address) as res:
                            pass
                case FetcherType.POST:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(url=fetcher.address, data=fetcher.fetch_data) as res:
                            pass
                case FetcherType.PING:
                    res = await ping(fetcher.address)
        except Exception:
            pass

        metric = ApSchedulerService.create_metric(prev, fetcher, res)
        with session_factory() as session:
            session.add(metric)
            session.commit()
            if not metric.ok:
                await self.process_fail(fetcher, metric, res)

        self.scheduler.reschedule_job(
            f"{fetcher.address} {fetcher.create_ts}",
            seconds=fetcher.delay_ok if metric.ok else fetcher.delay_fail,
            trigger="interval",
        )
