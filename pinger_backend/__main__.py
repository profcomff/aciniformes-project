import asyncio

from pinger_backend.service.crud import CrudService
from pinger_backend.service.scheduler import ApSchedulerService


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(ApSchedulerService(CrudService()).start())
    loop.run_forever()
