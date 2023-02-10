from fastapi import FastAPI, Depends
from aiogram.bot.bot import Bot
from functools import lru_cache
from alert_bot.settings import get_settings
from pydantic import BaseModel
from datetime import datetime

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
