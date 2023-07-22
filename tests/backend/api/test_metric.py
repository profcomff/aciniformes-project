
import pytest
from starlette import status
from aciniformes_backend.serivce.metric import PgMetricService


@pytest.fixture
def this_metric(dbsession):
    body = {"id": 5, "name": "string", "ok": True, "time_delta": 0}
    return body


class TestMetric:
    _url = "/metric"

    def test_post_success(self, client):
        body = {"name": "string", "ok": True, "time_delta": 0}
        print(self._url)
        res = client.post(self._url, json=body)
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["id"] is not None
        assert res_body["name"] == body["name"]
        assert res_body["ok"] == body["ok"]
        assert res_body["time_delta"] == body["time_delta"]

    def test_get_by_id_success(self, client, this_metric):
        res = client.get(f"{self._url}/{this_metric['id']}")
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["name"] == this_metric["name"]

    def test_get_success(self, client, this_metric):
        res = client.get(self._url)
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json())

    def test_get_by_id_not_found(self, client):
        res = client.get(f"{self._url}/{333}")
        assert res.status_code == status.HTTP_404_NOT_FOUND
