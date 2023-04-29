import pytest
from fastapi.testclient import TestClient

from aciniformes_backend.routes import app
from ping.service import Config


@pytest.fixture(scope="session")
def fake_config():
    Config.fake = False
    conf = Config()
    yield conf


@pytest.fixture(scope="session")
def crud_client():
    client = TestClient(app)
    return client
