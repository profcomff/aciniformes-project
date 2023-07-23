import pytest_asyncio
from starlette import status

from aciniformes_backend.serivce.metric import PgMetricService


metric = {"name": "string", "ok": True, "time_delta": 0}


@pytest_asyncio.fixture
async def this_metric(dbsession):
    yield await PgMetricService(dbsession).create(item=metric)


class TestMetric:
    _url = "/metric"

    def test_post_success(self, crud_client):
        body = {"name": "string", "ok": True, "time_delta": 0}
        res = crud_client.post(self._url, json=body)
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["id"] is not None
        assert res_body["name"] == body["name"]
        assert res_body["ok"] == body["ok"]
        assert res_body["time_delta"] == body["time_delta"]

    def test_get_by_id_success(self, crud_client, this_metric):
        res = crud_client.get(f"{self._url}/{this_metric}")
        assert res.status_code == status.HTTP_200_OK
        for k, v in metric.items():
            assert v == res.json()[k]

    def test_get_success(self, crud_client, this_metric):
        res = crud_client.get(self._url)
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json())
        get = crud_client.get(f"{self._url}/{this_metric}")
        assert res.status_code == status.HTTP_200_OK
        assert get.json() in res.json()

    def test_get_by_id_not_found(self, crud_client, this_metric):
        res = crud_client.get(f"{self._url}/{this_metric+2}")
        assert res.status_code == status.HTTP_404_NOT_FOUND
