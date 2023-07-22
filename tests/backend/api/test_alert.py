import json

import pytest
from starlette import status
import pytest_asyncio

from aciniformes_backend.serivce.alert import PgAlertService
from aciniformes_backend.serivce.receiver import PgReceiverService
from aciniformes_backend.settings import get_settings
from copy import deepcopy

alert = {
        "data": {"type": "string", "name": "string"},
        "filter": "string",
    }

@pytest_asyncio.fixture
async def this_alert(dbsession):
    global alert
    _alert = await PgAlertService(dbsession).create(item=alert)
    return _alert


class TestAlert:
    _url = "/alert"
    settings = get_settings()

    def test_post_success(self, client):
        body = {
            "data": {"type": "string", "name": "string"},
            "filter": "string",
        }
        res = client.post(self._url, json=body)
        res_body = res.json()
        assert res.status_code == status.HTTP_200_OK
        assert res_body["data"] == body["data"]
        assert res_body["filter"] == body["filter"]

    def test_get_by_id_success(self, client, this_alert):
        res = client.get(f"{self._url}/{this_alert}")
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["data"] == alert["data"]
        assert res_body["filter"] == alert["filter"]

    def test_delete_by_id_success(self, client, this_alert):
        res = client.delete(f"{self._url}/{this_alert}")
        assert res.status_code == status.HTTP_200_OK
        get = client.get(f"{self._url}/{this_alert}")
        assert get.status_code == status.HTTP_404_NOT_FOUND

    def test_get_success(self, client, this_alert):
        res = client.get(self._url)
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert len(res_body)
        get = client.get(f"{self._url}/{this_alert}")
        assert get.json() in res_body

    def test_patch_by_id_success(self, client, this_alert):
        body = {
            "data": {"type": "string", "name": "string"},
            "filter": "string",
        }
        res = client.patch(f"{self._url}/{this_alert}", data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["data"] == body["data"]
        get = client.get(f"{self._url}/{this_alert}")
        assert get.status_code == status.HTTP_200_OK
        assert get.json() == res_body

    def test_get_by_id_not_found(self, client, this_alert):
        res = client.get(f"{self._url}/{this_alert+2}")
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_by_id_not_found(self, client, this_alert):
        body = {
            "data": {"type": "string", "name": "string"},
            "filter": "string",
        }
        res = client.patch(f"{self._url}/{888}", data=json.dumps(body))
        assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.fixture
def this_receiver(dbsession):
    body = {"id": 4, "url": "string", "method": "post", "receiver_body": {}}
    return body


class TestReceiver:
    _url = "/receiver"

    def test_post_success(self, client):
        body = {"url": "string", "method": "post", "receiver_body": {}}
        res = client.post(self._url, json=body)
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["url"] == body["url"]
        assert res_body["receiver_body"] == body["receiver_body"]

    def test_get_by_id_success(self, client, this_receiver):
        res = client.get(f"{self._url}/{this_receiver['id']}")
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["url"] == this_receiver["url"]
        assert res_body["receiver_body"] == this_receiver["receiver_body"]

    def test_delete_by_id_success(self, client, this_receiver):
        res = client.delete(f"{self._url}/{this_receiver['id']}")
        assert res.status_code == status.HTTP_200_OK
        assert self.s.repository[this_receiver["id"]] is None

    def test_get_success(self, client, this_receiver):
        res = client.get(self._url)
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json())

    def test_patch_by_id_success(self, client, this_receiver):
        body = {"url": "sdasd", "method": "post", "receiver_body": {}}
        res = client.patch(
            f"{self._url}/{this_receiver['id']}",
            data=json.dumps(body),
        )
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["url"] == body["url"]
        assert res_body["receiver_body"] == body["receiver_body"]

    def test_get_by_id_not_found(self, client):
        res = client.get(f"{self._url}/{888}")
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_by_id_not_found(self, client):
        body = {"url": "sdasd", "method": "post", "receiver_body": {}}
        res = client.patch(f"{self._url}/{888}", data=json.dumps(body))
        assert res.status_code == status.HTTP_404_NOT_FOUND
