import uvicorn
from aiogram import executor

from .asgi import app, dp

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
