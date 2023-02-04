from ping.service import (
    SchedulerServiceInterface,
    scheduler_service,
)
from fastapi import FastAPI, Depends

ping_app = FastAPI()


@ping_app.get(
    "/start",
)
async def start_scheduler(
    scheduler: SchedulerServiceInterface = Depends(scheduler_service),
):
    await scheduler.start()


@ping_app.get("/fetchers")
async def get_fetchers(
    scheduler: SchedulerServiceInterface = Depends(scheduler_service),
):
    return await scheduler.crud_service.get_fetchers()


@ping_app.post("/schedule")
async def schedule_all_fetchers_from_db(
    scheduler: SchedulerServiceInterface = Depends(scheduler_service),
):
    fetchers = await scheduler.crud_service.get_fetchers()
    for fetcher in fetchers:
        await scheduler.add_fetcher(fetcher)


@ping_app.delete("/schedule")
async def delete_all_fetchers_from_scheduler(
    scheduler: SchedulerServiceInterface = Depends(scheduler_service),
):
    for f in await scheduler.crud_service.get_fetchers():
        await scheduler.delete_fetcher(f)


@ping_app.get("/stop")
async def stop_scheduler(
        scheduler: SchedulerServiceInterface = Depends(scheduler_service)
):
    await scheduler.stop()
