import pytest

from ping.service import Config, crud_service, scheduler_service


@pytest.fixture
def pg_config():
    Config.fake = True
    yield Config()


@pytest.fixture
def pg_scheduler_service(pg_config):
    s = scheduler_service()
    assert s.scheduler is not dict
    yield s


@pytest.fixture
def fake_crud_service(pg_config):
    Config.fake = True
    s = crud_service()
    yield s
    Config.fake = False
