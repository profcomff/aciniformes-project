import pytest
import pytest_asyncio
from starlette import status

from aciniformes_backend.service.metric import PgMetricService


metric = {"name": "string", "ok": True, "time_delta": 0}


@pytest_asyncio.fixture
async def this_metric(dbsession):
    yield await PgMetricService(dbsession).create(item=metric)


@pytest.mark.authenticated("pinger.metric.create")
def test_post_success(crud_client):
    body = {"name": "string", "ok": True, "time_delta": 0}
    res = crud_client.post("/metric", json=body)
    assert res.status_code == status.HTTP_200_OK
    res_body = res.json()
    assert res_body["id"] is not None
    assert res_body["name"] == body["name"]
    assert res_body["ok"] == body["ok"]
    assert res_body["time_delta"] == body["time_delta"]


@pytest.mark.authenticated("pinger.metric.read")
def test_get_by_id_success(crud_client, this_metric):
    res = crud_client.get(f"/metric/{this_metric}")
    assert res.status_code == status.HTTP_200_OK
    for k, v in metric.items():
        assert v == res.json()[k]


@pytest.mark.authenticated("pinger.metric.read")
def test_get_success(crud_client, this_metric):
    res = crud_client.get("/metric")
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json())
    get = crud_client.get(f"/metric/{this_metric}")
    assert res.status_code == status.HTTP_200_OK
    assert get.json() in res.json()


@pytest.mark.authenticated("pinger.metric.read")
def test_get_by_id_not_found(crud_client, this_metric):
    res = crud_client.get(f"/metric/{this_metric+2}")
    assert res.status_code == status.HTTP_404_NOT_FOUND
