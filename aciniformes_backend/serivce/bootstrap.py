from .metric import PgMetricService
from .alert import PgAlertService
from .receiver import PgReceiverService
from fastapi_sqlalchemy import db


def pg_metric_service():
    return PgMetricService(db.session)


def pg_alert_service():
    return PgAlertService(db.session)


def pg_receiver_service():
    return PgReceiverService(db.session)
