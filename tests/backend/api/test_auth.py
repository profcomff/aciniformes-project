import json

import pytest
import sqlalchemy
from starlette import status

from aciniformes_backend.models import Auth
from aciniformes_backend.serivce import auth_service


def test_auth_service(fake_config):
    s = auth_service()
    assert s.session is None
    assert type(s.repository) is list


@pytest.fixture
def registered_user(client):
    body = {"username": "test", "password": "test"}
    res = client.post("/auth/register", data=json.dumps(body))
    assert res.status_code == status.HTTP_201_CREATED


class TestAuth:
    _url = "/auth"

    def test_create_user(self, dbsession, client):
        body = {"username": "test", "password": "test"}
        res = client.post("/auth/register", data=json.dumps(body))
        assert res.status_code == status.HTTP_201_CREATED
