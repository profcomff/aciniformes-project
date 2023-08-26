import asyncio
import signal
from logging.config import fileConfig
from pathlib import Path

from aciniformes_backend.settings import get_settings

from .service.scheduler import ApSchedulerService


path = Path(__file__).resolve().parents[1]


fileConfig(f"{path}/logging_pinger.conf")


def sigint_callback(scheduler: ApSchedulerService) -> None:
    scheduler.stop()
    exit(0)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    scheduler = ApSchedulerService()
    scheduler.backend_url = get_settings().BACKEND_URL
    loop.add_signal_handler(signal.SIGINT, callback=lambda: sigint_callback(scheduler))
    loop.create_task(scheduler.start())
    loop.run_forever()
