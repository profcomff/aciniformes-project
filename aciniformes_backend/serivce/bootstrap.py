from fastapi_sqlalchemy import db
from .metric import PgMetricService
from .alert import PgAlertService
from .receiver import PgReceiverService
from .fetcher import PgFetcherService
from .fake import (
    FakeAlertService,
    FakeMetricService,
    FakeReceiverSerivce,
    FakeFetcherService,
)


class Config:
    fake: bool = False


def metric_service():
    if Config.fake:
        return FakeMetricService(None)
    return PgMetricService(db.session)


def alert_service():
    if Config.fake:
        return FakeAlertService(None)
    return PgAlertService(db.session)


def receiver_service():
    if Config.fake:
        return FakeReceiverSerivce(None)
    return PgReceiverService(db.session)


def fetcher_service():
    if Config.fake:
        return FakeFetcherService(None)
    return PgFetcherService(db.session)
