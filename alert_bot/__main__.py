from aiogram import executor
from .asgi import BotScheduler
import asyncio
from ping.service.crud import FakeCrudService

from .asgi import app, dp

if __name__ == "__main__":
    asyncio.run(BotScheduler(FakeCrudService()).start())
    # executor.start_polling(dp, skip_updates=True)
