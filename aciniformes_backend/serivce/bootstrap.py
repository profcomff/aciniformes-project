from fastapi_sqlalchemy import db

from .alert import PgAlertService
from .fake import FakeAlertService, FakeFetcherService, FakeMetricService, FakeReceiverService
from .fetcher import PgFetcherService
from .metric import PgMetricService
from .receiver import PgReceiverService


class Config:
    fake: bool = False


def metric_service():
    if Config.fake:
        return FakeMetricService(None)
    with db():
        return PgMetricService(db.session)


def alert_service():
    if Config.fake:
        return FakeAlertService(None)
    with db():
        return PgAlertService(db.session)


def receiver_service():
    if Config.fake:
        return FakeReceiverService(None)
    with db():
        return PgReceiverService(db.session)


def fetcher_service():
    if Config.fake:
        return FakeFetcherService(None)
    with db():
        return PgFetcherService(db.session)
