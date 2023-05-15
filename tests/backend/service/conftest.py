import pytest

from aciniformes_backend.serivce import Config, alert_service, fetcher_service, metric_service, receiver_service


@pytest.fixture
def pg_config():
    Config.fake = False
    yield Config()


@pytest.fixture
def pg_alert_service(pg_config):
    s = alert_service()
    assert s.session is not None
    yield s


@pytest.fixture
def pg_fetcher_service(pg_config):
    s = fetcher_service()
    assert s.session is not None
    yield s


@pytest.fixture
def pg_receiver_service(pg_config):
    s = receiver_service()
    assert s.session is not None
    yield s


@pytest.fixture
def pg_metric_service(pg_config):
    s = metric_service()
    assert s.session is not None
    yield s
