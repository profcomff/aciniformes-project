import argparse
import logging
from time import sleep

import uvicorn

from .routes import app

logger = logging.getLogger(__name__)


def get_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    run_api = subparsers.add_parser("run_api")
    run_scheduller = subparsers.add_parser("run_scheduller")
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    args = get_args()
    logger.info(vars(args))

    if args.command == 'run_api':
        logger.info("Starting API")
        uvicorn.run(app)
        exit(0)

    if args.command == 'run_scheduller':
        logger.info("Starting Scheduller")
        while True:
            logger.info("PING!")
            sleep(100)
