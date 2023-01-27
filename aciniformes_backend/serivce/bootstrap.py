from fastapi_sqlalchemy import db
from .metric import PgMetricService
from .alert import PgAlertService
from .receiver import PgReceiverService
from .fetcher import PgFetcherService
from .fake import (
    FakeAlertService,
    FakeMetricService,
    FakeReceiverService,
    FakeFetcherService,
)


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
