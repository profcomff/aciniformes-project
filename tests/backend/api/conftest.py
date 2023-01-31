import pytest

from aciniformes_backend.serivce import (
    metric_service,
    alert_service,
    receiver_service,
    fetcher_service,
)


@pytest.fixture
def fake_metric_service(service_config):
    s = metric_service()
    assert s.session is None
    assert type(s.repository) == dict
    yield s
