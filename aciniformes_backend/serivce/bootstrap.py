from fastapi_sqlalchemy import db

from .alert import PgAlertService
from .fetcher import PgFetcherService
from .metric import PgMetricService
from .receiver import PgReceiverService


def metric_service():
    return PgMetricService(db.session)


def alert_service():
    return PgAlertService(db.session)


def receiver_service():
    return PgReceiverService(db.session)


def fetcher_service():
    return PgFetcherService(db.session)
