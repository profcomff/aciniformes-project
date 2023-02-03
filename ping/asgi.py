import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from fastapi import FastAPI

ping_app = FastAPI()


def foo():
    print("foo")


def bar():
    print("bar")


s: AsyncIOScheduler = AsyncIOScheduler()


@ping_app.get("/")
async def gg():
    s.add_job(foo, 'interval', seconds=3)
    s.start()


@ping_app.get("/stop")
async def stop():
    s.shutdown()
