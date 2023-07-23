import pytest

from pinger_backend.service.scheduler import ApSchedulerService, CrudService


@pytest.fixture
def pg_scheduler_service():
    s = ApSchedulerService(CrudService())
    s.backend_url = "http://testserver"
    assert s.scheduler is not dict
    yield s
