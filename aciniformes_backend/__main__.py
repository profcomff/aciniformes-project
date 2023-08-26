from logging.config import fileConfig
fileConfig('./logging_prod.conf')

from .cli import process


if __name__ == "__main__":
    process()
