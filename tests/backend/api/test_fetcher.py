import json
from copy import deepcopy

import pytest_asyncio
from starlette import status

from aciniformes_backend.serivce.fetcher import PgFetcherService


fetcher = {
    "type_": "ping",
    "address": "https://www.python.org",
    "fetch_data": "string",
    "delay_ok": 30,
    "delay_fail": 40,
}


@pytest_asyncio.fixture
async def this_fetcher(dbsession):
    yield await PgFetcherService(dbsession).create(item=fetcher)


class TestFetcher:
    _url = "/fetcher"

    def test_post_success(self, crud_client):
        body = {
            "type_": "get",
            "address": "string",
            "fetch_data": "string",
            "delay_ok": 300,
            "delay_fail": 30,
        }
        res = crud_client.post(self._url, json=body)
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["id"] is not None

    def test_get_by_id_success(self, crud_client, this_fetcher):
        res = crud_client.get(f"{self._url}/{this_fetcher}")
        assert res.status_code == status.HTTP_200_OK
        _new_fetcher = deepcopy(fetcher)
        for k, v in _new_fetcher.items():
            assert v == res.json()[k]

    def test_delete_by_id_success(self, crud_client, this_fetcher):
        res = crud_client.delete(f"{self._url}/{this_fetcher}")
        assert res.status_code == status.HTTP_200_OK
        res = crud_client.get(f"{self._url}/{this_fetcher}")
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_get_success(self, crud_client, this_fetcher):
        res = crud_client.get(self._url)
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json())
        get = crud_client.get(f"{self._url}/{this_fetcher}")
        assert get.status_code == status.HTTP_200_OK
        assert get.json() in res.json()

    def test_patch_by_id_success(self, crud_client, this_fetcher):
        body = {
            "type_": "post",
            "address": "https://api.test.profcomff.com/services/category",
            "fetch_data": "string",
            "delay_ok": 300,
            "delay_fail": 30,
        }
        res = crud_client.patch(
            f"{self._url}/{this_fetcher}",
            json=body,
        )
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["address"] == body["address"]
        assert res_body["type_"] == body["type_"]
        res = crud_client.get(f"{self._url}/{this_fetcher}")
        assert res.status_code == status.HTTP_200_OK
        for k, v in body.items():
            assert v == res.json()[k]

    def test_get_by_id_not_found(self, crud_client):
        res = crud_client.get(f"{self._url}/{888}")
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_by_id_not_found(self, crud_client):
        body = {
            "type_": "post",
            "address": "https://api.test.profcomff.com/services/category",
            "fetch_data": "string",
            "delay_ok": 300,
            "delay_fail": 30,
        }
        res = crud_client.patch(f"{self._url}/{888}", data=json.dumps(body))
        assert res.status_code == status.HTTP_404_NOT_FOUND
