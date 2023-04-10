import json

import pytest
from starlette import status

from aciniformes_backend.serivce import Config, metric_service


@pytest.fixture
def this_metric():
    body = {"id": 44, "metrics": {}}
    metric_service().repository[body["id"]] = body
    return body


class TestMetric:
    _url = "/metric"
    Config.fake = True
    s = metric_service()

    def test_post_success(self, client):
        body = {"metrics": {}}
        res = client.post(self._url, data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["id"] is not None
        assert res_body["metrics"] == body["metrics"]

    def test_get_by_id_success(self, client, this_metric):
        res = client.get(f"{self._url}/{this_metric['id']}")
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["metrics"] == this_metric["metrics"]

    def test_get_success(self, client, this_metric):
        res = client.get(self._url)
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json())

    def test_get_by_id_not_found(self, client):
        res = client.get(f"{self._url}/{333}")
        assert res.status_code == status.HTTP_404_NOT_FOUND
