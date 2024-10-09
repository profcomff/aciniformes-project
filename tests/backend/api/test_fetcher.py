import json
from copy import deepcopy

import pytest
import pytest_asyncio
import sqlalchemy as sa
from starlette import status

import aciniformes_backend.models as db_models


fetcher = {
    "type_": "ping",
    "address": "https://www.python.org",
    "fetch_data": "string",
    "delay_ok": 30,
    "delay_fail": 40,
}


@pytest_asyncio.fixture
async def this_fetcher(dbsession):
    global fetcher
    q = sa.insert(db_models.Fetcher).values(**fetcher).returning(db_models.Fetcher)
    fetcher = dbsession.scalar(q)
    dbsession.flush()

    yield fetcher.id_

    q = sa.delete(db_models.Fetcher).where(db_models.Fetcher.id_ == id)
    dbsession.execute(q)
    dbsession.flush()


@pytest.mark.authenticated("pinger.fetcher.create")
def test_post_success(crud_client):
    body = {
        "type_": "get",
        "address": "https://google.com",
        "fetch_data": "string",
        "delay_ok": 300,
        "delay_fail": 30,
    }
    res = crud_client.post("/fetcher", json=body)
    assert res.status_code == status.HTTP_200_OK
    res_body = res.json()
    assert res_body["id"] is not None


@pytest.mark.authenticated("pinger.fetcher.read")
def test_get_by_id_success(crud_client, this_fetcher):
    global fetcher
    res = crud_client.get(f"/fetcher/{this_fetcher}")
    assert res.status_code == status.HTTP_200_OK
    _new_fetcher = deepcopy(fetcher)
    for k, v in _new_fetcher.items():
        assert v == res.json()[k]


@pytest.mark.authenticated("pinger.fetcher.read", "pinger.fetcher.delete")
def test_delete_by_id_success(crud_client, this_fetcher):
    res = crud_client.delete(f"/fetcher/{this_fetcher}")
    assert res.status_code == status.HTTP_200_OK
    res = crud_client.get(f"/fetcher/{this_fetcher}")
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.authenticated("pinger.fetcher.read")
def test_get_success(crud_client, this_fetcher):
    res = crud_client.get("/fetcher")
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json())
    get = crud_client.get(f"/fetcher/{this_fetcher}")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() in res.json()


@pytest.mark.authenticated("pinger.fetcher.read", "pinger.fetcher.update")
def test_patch_by_id_success(crud_client, this_fetcher):
    body = {
        "type_": "post",
        "address": "https://api.test.profcomff.com/services/category",
        "fetch_data": "string",
        "delay_ok": 300,
        "delay_fail": 30,
    }
    res = crud_client.patch(
        f"/fetcher/{this_fetcher}",
        json=body,
    )
    assert res.status_code == status.HTTP_200_OK
    res_body = res.json()
    assert res_body["address"] == body["address"]
    assert res_body["type_"] == body["type_"]
    res = crud_client.get(f"/fetcher/{this_fetcher}")
    assert res.status_code == status.HTTP_200_OK
    for k, v in body.items():
        assert v == res.json()[k]


@pytest.mark.authenticated("pinger.fetcher.read")
def test_get_by_id_not_found(crud_client):
    res = crud_client.get(f"/fetcher/{888}")
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.authenticated("pinger.fetcher.update")
def test_patch_by_id_not_found(crud_client):
    body = {
        "type_": "post",
        "address": "https://api.test.profcomff.com/services/category",
        "fetch_data": "string",
        "delay_ok": 300,
        "delay_fail": 30,
    }
    res = crud_client.patch(f"/fetcher/{888}", data=json.dumps(body))
    assert res.status_code == status.HTTP_404_NOT_FOUND
