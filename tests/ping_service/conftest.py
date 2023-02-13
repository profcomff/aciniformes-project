import pytest
from ping.api.asgi import ping_app
from fastapi.testclient import TestClient
from ping.service import Config
from aciniformes_backend.routes import app


@pytest.fixture(scope="session")
def fake_config():
    Config.fake = True
    conf = Config()
    yield conf


@pytest.fixture(scope="session")
def crud_client():
    client = TestClient(app)
    return client


@pytest.fixture(scope="session")
def ping_client(fake_config):
    client = TestClient(ping_app)
    return client
