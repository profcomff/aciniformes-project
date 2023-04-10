from datetime import datetime
from functools import lru_cache

from aiogram.bot.bot import Bot
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from alert_bot.settings import get_settings

app = FastAPI()


class AlertPostSchema(BaseModel):
    receiver_id: str
    data: str
    timestamp: datetime


@lru_cache(None)
def get_bot():
    return Bot(get_settings().BOT_TOKEN)


@app.post("/alert")
async def post_alert(alert: AlertPostSchema, bot: Bot = Depends(get_bot)):
    await bot.send_message(alert.receiver_id, str(alert.data) + str(alert.timestamp))
