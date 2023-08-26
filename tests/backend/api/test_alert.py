import json
import pytest

import pytest_asyncio
from starlette import status

from aciniformes_backend.serivce.alert import PgAlertService
from settings import get_settings

settings = get_settings()


alert = {
    "data": {"type": "string", "name": "string"},
    "filter": "string",
}


@pytest_asyncio.fixture
async def this_alert(dbsession):
    global alert
    _alert = await PgAlertService(dbsession).create(item=alert)
    yield _alert


@pytest.mark.authenticated("pinger.alert.create")
def test_post_success(crud_client):
    body = {
        "data": {"type": "string", "name": "string"},
        "filter": "string",
    }
    res = crud_client.post("/alert", json=body)
    res_body = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert res_body["data"] == body["data"]
    assert res_body["filter"] == body["filter"]


@pytest.mark.authenticated("pinger.alert.read")
def test_get_by_id_success(crud_client, this_alert):
    res = crud_client.get(f"/alert/{this_alert}")
    assert res.status_code == status.HTTP_200_OK
    res_body = res.json()
    assert res_body["data"] == alert["data"]
    assert res_body["filter"] == alert["filter"]


@pytest.mark.authenticated("pinger.alert.read", "pinger.alert.delete")
def test_delete_by_id_success(crud_client, this_alert):
    res = crud_client.delete(f"/alert/{this_alert}")
    assert res.status_code == status.HTTP_200_OK
    get = crud_client.get(f"/alert/{this_alert}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.authenticated("pinger.alert.read")
def test_get_success(crud_client, this_alert):
    res = crud_client.get("/alert")
    assert res.status_code == status.HTTP_200_OK
    res_body = res.json()
    assert len(res_body)
    get = crud_client.get(f"/alert/{this_alert}")
    assert get.json() in res_body


@pytest.mark.authenticated("pinger.alert.read", "pinger.alert.update")
def test_patch_by_id_success(crud_client, this_alert):
    body = {
        "data": {"type": "string", "name": "string"},
        "filter": "string",
    }
    res = crud_client.patch(f"/alert/{this_alert}", data=json.dumps(body))
    assert res.status_code == status.HTTP_200_OK
    res_body = res.json()
    assert res_body["data"] == body["data"]
    get = crud_client.get(f"/alert/{this_alert}")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == res_body


@pytest.mark.authenticated("pinger.alert.read")
def test_get_by_id_not_found(crud_client, this_alert):
    res = crud_client.get(f"/alert/{this_alert+2}")
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.authenticated("pinger.alert.read", "pinger.alert.update")
def test_patch_by_id_not_found(crud_client, this_alert):
    body = {
        "data": {"type": "string", "name": "string"},
        "filter": "string",
    }
    res = crud_client.patch(f"/alert/{888}", data=json.dumps(body))
    assert res.status_code == status.HTTP_404_NOT_FOUND
