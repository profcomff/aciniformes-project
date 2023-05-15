import asyncio

from pinger_backend.service.scheduler import ApSchedulerService
from pinger_backend.service.crud import CrudService

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(ApSchedulerService(CrudService()).start())
    loop.run_forever()
