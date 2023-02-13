from ping.service import Config, scheduler_service, crud_service
import pytest


@pytest.fixture
def pg_config():
    Config.fake = False
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
