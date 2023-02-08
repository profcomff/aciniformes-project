from fastapi import FastAPI, Depends
from aciniformes_backend.models import Alert
from aiogram.bot.bot import Bot
from functools import lru_cache
from alert_bot.settings import get_settings
app = FastAPI()


@lru_cache(None)
def get_bot():
    return Bot(get_settings().BOT_TOKEN)


@app.post("/alert")
async def post_alert(alert: dict, bot: Bot = Depends(get_bot)):
    await bot.send_message(alert.receiver, str(alert.data))

