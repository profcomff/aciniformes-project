import json

import pytest


@pytest.fixture
def auth_user(client):
    body = {"username": "test", "password": "test"}
    res = client.post("/auth/register", data=json.dumps(body))
    assert res.status_code == 201
    return body


@pytest.fixture
def auth_header(client, auth_user):
    beaver = client.post(
        f"/auth/token",
        data={
            "username": auth_user["username"],
            "password": auth_user["password"],
            "grant_type": "password",
        },
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert beaver.status_code == 200
    auth_data = json.loads(beaver.content)
    auth_headers = {"Authorization": f"Bearer {auth_data.get('access_token')}"}
    return auth_headers
