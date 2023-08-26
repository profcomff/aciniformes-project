import argparse
import logging
from logging.config import fileConfig


logger = logging.getLogger(__name__)


def get_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser("api")
    worker = subparsers.add_parser("worker")
    worker.add_argument('--logger-config', type=str, default='./logging_dev.conf')

    return parser.parse_args()


def process():
    args = get_args()

    if args.command == "api":
        import uvicorn
        from aciniformes_backend.routes import app

        logger.debug("API starting")
        uvicorn.run(app)
        exit(0)

    if args.command == "worker":
        import asyncio
        import signal
        from aciniformes_backend.worker.service.scheduler import ApSchedulerService

        fileConfig(args.logger_config, disable_existing_loggers=True)

        def sigint_callback(scheduler: ApSchedulerService) -> None:
            scheduler.stop()
            exit(0)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        scheduler = ApSchedulerService()
        loop.add_signal_handler(signal.SIGINT, callback=lambda: sigint_callback(scheduler))

        logger.debug("Worker starting")
        loop.create_task(scheduler.start())
        loop.run_forever()
