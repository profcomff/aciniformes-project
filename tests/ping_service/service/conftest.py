import pytest

from aciniformes_backend.worker.scheduler import ApSchedulerService


@pytest.fixture
def pg_scheduler_service():
    s = ApSchedulerService()
    s.backend_url = "http://testserver"
    assert s.scheduler is not dict
    yield s
