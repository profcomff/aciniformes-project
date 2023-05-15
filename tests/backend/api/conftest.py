import pytest
from fastapi.testclient import TestClient

from aciniformes_backend.routes.base import app


@pytest.fixture
def client():
    client = TestClient(app)
    return client
