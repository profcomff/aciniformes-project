import pytest

from pinger_backend.service.scheduler import ApSchedulerService


@pytest.fixture
def pg_scheduler_service():
    s = ApSchedulerService()
    s.backend_url = "http://testserver"
    assert s.scheduler is not dict
    yield s
