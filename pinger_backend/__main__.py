import asyncio

from service.crud import CrudService
from service.scheduler import ApSchedulerService

from settings import get_settings


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    scheduler = ApSchedulerService(CrudService())
    scheduler.backend_url = get_settings().BACKEND_URL
    loop.create_task(scheduler.start())
    loop.run_forever()
