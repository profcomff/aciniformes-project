import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from aciniformes_backend.routes.base import app


@pytest.fixture
def client(mocker: MockerFixture):
    user_mock = mocker.patch("auth_lib.fastapi.UnionAuth.__call__")
    user_mock.return_value = {
        "session_scopes": [
            {"id": 53, "name": "pinger.alert.create"},
            {"id": 56, "name": "pinger.receiver.create"},
            {"id": 61, "name": "pinger.fetcher.update"},
            {"id": 62, "name": "pinger.metric.create"},
            {"id": 60, "name": "pinger.fetcher.delete"},
            {"id": 57, "name": "pinger.receiver.delete"},
            {"id": 54, "name": "pinger.alert.delete"},
            {"id": 58, "name": "pinger.receiver.update"},
            {"id": 59, "name": "pinger.fetcher.create"},
            {"id": 55, "name": "pinger.alert.update"},
        ],
        "user_scopes": [
            {"id": 53, "name": "pinger.alert.create"},
            {"id": 56, "name": "pinger.receiver.create"},
            {"id": 61, "name": "pinger.fetcher.update"},
            {"id": 62, "name": "pinger.metric.create"},
            {"id": 60, "name": "pinger.fetcher.delete"},
            {"id": 57, "name": "pinger.receiver.delete"},
            {"id": 54, "name": "pinger.alert.delete"},
            {"id": 58, "name": "pinger.receiver.update"},
            {"id": 59, "name": "pinger.fetcher.create"},
            {"id": 55, "name": "pinger.alert.update"},
        ],
        "indirect_groups": [{"id": 0, "name": "string", "parent_id": 0}],
        "groups": [{"id": 0, "name": "string", "parent_id": 0}],
        "id": 0,
        "email": "string",
    }
    client = TestClient(app)
    return client
