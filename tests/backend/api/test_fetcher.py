import json

import pytest
from starlette import status

from aciniformes_backend.serivce import Config, fetcher_service


def test_fake_service(fake_config):
    s = fetcher_service()
    assert s.session is None
    assert type(s.repository) is dict


@pytest.fixture
def this_fetcher():
    body = {
        "id": 6,
        "type_": "get",
        "address": "string",
        "fetch_data": "string",
        "delay_ok": 0,
        "delay_fail": 0,
    }
    fetcher_service().repository[body["id"]] = body
    return body


class TestFetcher:
    _url = "/fetcher"
    Config.fake = True
    s = fetcher_service()

    def test_post_success(self, client):
        body = {
            "type_": "get",
            "address": "string",
            "fetch_data": "string",
            "delay_ok": 300,
            "delay_fail": 30,
        }
        res = client.post(self._url, json=body)
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["id"] is not None

    def test_get_by_id_success(self, client, this_fetcher):
        res = client.get(f"{self._url}/{this_fetcher['id']}")
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["address"] == this_fetcher["address"]

    def test_delete_by_id_success(self, client, this_fetcher):
        res = client.delete(f"{self._url}/{this_fetcher['id']}")
        assert res.status_code == status.HTTP_200_OK
        assert self.s.repository[this_fetcher["id"]] is None

    def test_get_success(self, client, this_fetcher):
        res = client.get(self._url)
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json())

    def test_patch_by_id_success(self, client, this_fetcher):
        body = {
              "type_": "post",
              "address": "https://api.test.profcomff.com/services/category",
              "fetch_data": "string",
              "delay_ok": 300,
              "delay_fail": 30
            }
        res = client.patch(
            f"{self._url}/{this_fetcher['id']}",
            json=body,
        )
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["address"] == body["address"]
        assert res_body["type_"] == body["type_"]

    def test_get_by_id_not_found(self, client):
        res = client.get(f"{self._url}/{888}")
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_by_id_not_found(self, client):
        body = {"name": "s"}
        res = client.patch(f"{self._url}/{888}", data=json.dumps(body))
        assert res.status_code == status.HTTP_404_NOT_FOUND
