import time
from datetime import datetime

import httpx
from aiogram import Bot, Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from pydantic import BaseModel

from aciniformes_backend.models import Alert, Fetcher, FetcherType
from aciniformes_backend.routes.mectric import CreateSchema as MetricCreateSchema
from aciniformes_backend.routes.alert.alert import CreateSchema as AlertCreateSchema
from alert_bot.settings import get_settings
from ping.service.crud import CrudServiceInterface, FakeCrudService
from ping.service.exceptions import AlreadyRunning
from ping.service.scheduler import SchedulerServiceInterface

bot = Bot(get_settings().BOT_TOKEN)
app = FastAPI()
settings = get_settings()
dp = Dispatcher(bot)


class BotScheduler(SchedulerServiceInterface):
    scheduler = AsyncIOScheduler()

    def __init__(self, crud_service: CrudServiceInterface):
        self.crud_service = crud_service

    async def add_fetcher(self, fetcher: Fetcher):
        self.scheduler.add_job(
            self._fetch_it,
            args=[fetcher],
            id=f"{fetcher.name} {fetcher.create_ts}",
            seconds=fetcher.delay_ok,
            trigger="interval",
        )

    async def delete_fetcher(self, fetcher: Fetcher):
        self.scheduler.remove_job(fetcher.name)

    async def get_jobs(self):
        return [j.id for j in self.scheduler.get_jobs()]

    async def start(self):
        if self.scheduler.running:
            raise AlreadyRunning
        fetchers = httpx.get(f"{settings.BACKEND_URL}/fetcher").json()
        self.scheduler.start()
        for fetcher in fetchers:
            fetcher = Fetcher(**fetcher)
            await self.add_fetcher(fetcher)
            await self._fetch_it(fetcher)

    async def stop(self):
        self.scheduler.shutdown()
        for job in self.scheduler.get_jobs():
            job.remove()

    async def write_alert(self, metric_log: MetricCreateSchema, alert: Alert):
        for receiver in httpx.get(f"{settings.BACKEND_URL}/receiver").json():
            await bot.send_message(
                chat_id=receiver["chat_id"], text=str(metric_log.metrics)
            )

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
            for receiver in httpx.get(f"{settings.BACKEND_URL}/receiver").json():
                print(receiver)
                alert = {'data': {
                    "status_code": 500,
                    "url": fetcher.address
                },
                         'receiver': receiver["chat_id"],
                         'filter': "fail"}
                httpx.post(f"{settings.BACKEND_URL}/alert", json=alert)
        cur = time.time()
        timing = cur - prev
        metric = MetricCreateSchema(
            metrics={
                "status_code": res.status_code if res else 500,
                "url": fetcher.address,
                "body": fetcher.fetch_data,
                "timing_ms": timing,
            }
        )
        self.scheduler.reschedule_job(
            f"{fetcher.name} {fetcher.create_ts}",
            seconds=fetcher.delay_ok,
            trigger="interval",
        )
        for alert in httpx.get(f"{settings.BACKEND_URL}/alert").json():
            print(alert)
            if alert.filter == str(res.status_code):
                self.scheduler.reschedule_job(
                    f"{fetcher.name} {fetcher.create_ts}",
                    seconds=fetcher.delay_fail,
                    trigger="interval",
                )
                await self.write_alert(metric, alert)
        await self.crud_service.add_metric(metric)


class AlertPostSchema(BaseModel):
    receiver_id: str
    data: str
    timestamp: datetime


class DataPostSchema(BaseModel):
    receiver_id: str
    data: str
    timestamp: datetime


class AuthPostSchema(BaseModel):
    receiver_id: str


@dp.message_handler(commands=["start_pinger"])
async def start_pinger(message: types.Message):
    token = message.get_args()
    if not token:
        await message.reply(
            "Для авторизации выполните команду еще раз вместе с токеном"
        )
        return False
    user_scopes = httpx.get(
        f"https://api.test.profcomff.com/auth/me?info=session_scopes", headers={"authorization": token}
    ).json()
    if {'id': 79, 'name': 'pinger.bot.start'} in user_scopes["session_scopes"]:
        body = {
            "name": message.get_current()["from"]["username"],
            "chat_id": message.get_current()["from"]["id"],
        }
        httpx.post(
            f"{settings.BACKEND_URL}/receiver", json=body
        )
        await BotScheduler(FakeCrudService()).start()
        fetchers = httpx.get(f"{settings.BACKEND_URL}/fetcher").json()
        text = "Успешные опросы: \n"
        for fetcher in fetchers:
            if fetcher["metrics"] != {}:
                text += str(fetcher["metrics"])
                text += '\n'
        await bot.send_message(
            chat_id=message.get_current()["from"]["id"], text=text
        )
    else:
        await message.reply(
            "У вас недостаточно прав для запуска бота"
        )


@dp.message_handler(commands=["stop_pinger"])
async def stop_pinger(message: types.Message):
    token = message.get_args()
    if not token:
        await message.reply(
            "Для авторизации выполните команду еще раз вместе с токеном"
        )
        return False
    scopes = httpx.get(
        f"https://api.test.profcomff.com/auth/me", headers={"authorization": token}
    )
    if scopes:
        await BotScheduler(FakeCrudService()).stop()
