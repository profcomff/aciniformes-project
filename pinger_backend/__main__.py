import asyncio

from pinger_backend.service.crud import CrudService
from pinger_backend.service.scheduler import ApSchedulerService

from .settings import get_settings


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    scheduler = ApSchedulerService(CrudService())
    scheduler.backend_url = get_settings().BACKEND_URL
    loop.create_task(scheduler.start())
    loop.run_forever()
