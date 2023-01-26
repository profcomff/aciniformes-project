import pytest
from aciniformes_backend.serivce import (
    alert_service,
    fetcher_service,
    receiver_service,
    metric_service,
    Config,
)


@pytest.fixture
def pg_config():
    Config.fake = False
    yield Config()


@pytest.fixture
def pg_alert_service(pg_config):
    s = alert_service()
    assert s.session is not None


@pytest.fixture
def pg_fetcher_service(pg_config):
    pass
