import json

import pytest_asyncio
from starlette import status

from aciniformes_backend.serivce.alert import PgAlertService
from aciniformes_backend.serivce.receiver import PgReceiverService
from settings import get_settings


alert = {
    "data": {"type": "string", "name": "string"},
    "filter": "string",
}


@pytest_asyncio.fixture
async def this_alert(dbsession):
    global alert
    _alert = await PgAlertService(dbsession).create(item=alert)
    yield _alert


class TestAlert:
    _url = "/alert"
    settings = get_settings()

    def test_post_success(self, crud_client):
        body = {
            "data": {"type": "string", "name": "string"},
            "filter": "string",
        }
        res = crud_client.post(self._url, json=body)
        res_body = res.json()
        assert res.status_code == status.HTTP_200_OK
        assert res_body["data"] == body["data"]
        assert res_body["filter"] == body["filter"]

    def test_get_by_id_success(self, crud_client, this_alert):
        res = crud_client.get(f"{self._url}/{this_alert}")
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["data"] == alert["data"]
        assert res_body["filter"] == alert["filter"]

    def test_delete_by_id_success(self, crud_client, this_alert):
        res = crud_client.delete(f"{self._url}/{this_alert}")
        assert res.status_code == status.HTTP_200_OK
        get = crud_client.get(f"{self._url}/{this_alert}")
        assert get.status_code == status.HTTP_404_NOT_FOUND

    def test_get_success(self, crud_client, this_alert):
        res = crud_client.get(self._url)
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert len(res_body)
        get = crud_client.get(f"{self._url}/{this_alert}")
        assert get.json() in res_body

    def test_patch_by_id_success(self, crud_client, this_alert):
        body = {
            "data": {"type": "string", "name": "string"},
            "filter": "string",
        }
        res = crud_client.patch(f"{self._url}/{this_alert}", data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["data"] == body["data"]
        get = crud_client.get(f"{self._url}/{this_alert}")
        assert get.status_code == status.HTTP_200_OK
        assert get.json() == res_body

    def test_get_by_id_not_found(self, crud_client, this_alert):
        res = crud_client.get(f"{self._url}/{this_alert+2}")
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_by_id_not_found(self, crud_client, this_alert):
        body = {
            "data": {"type": "string", "name": "string"},
            "filter": "string",
        }
        res = crud_client.patch(f"{self._url}/{888}", data=json.dumps(body))
        assert res.status_code == status.HTTP_404_NOT_FOUND


reciever = {"url": "https://google.com", "method": "post", "receiver_body": {}}


@pytest_asyncio.fixture
async def this_receiver(dbsession):
    global reciever
    _reciever = await PgReceiverService(dbsession).create(item=reciever)
    yield _reciever


class TestReceiver:
    _url = "/receiver"

    def test_post_success(self, crud_client):
        body = {"url": "https://google.com", "method": "post", "receiver_body": {}}
        res = crud_client.post(self._url, json=body)
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["url"] == body["url"]
        assert res_body["receiver_body"] == body["receiver_body"]

    def test_get_by_id_success(self, crud_client, this_receiver):
        res = crud_client.get(f"{self._url}/{this_receiver}")
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["url"] == reciever["url"]
        assert res_body["receiver_body"] == reciever["receiver_body"]

    def test_delete_by_id_success(self, crud_client, this_receiver):
        res = crud_client.delete(f"{self._url}/{this_receiver}")
        assert res.status_code == status.HTTP_200_OK
        res = crud_client.get(f"{self._url}/{this_receiver}")
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_get_success(self, crud_client, this_receiver):
        res = crud_client.get(self._url)
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json())
        get = crud_client.get(f"{self._url}/{this_receiver}")
        assert get.json() in res.json()

    def test_patch_by_id_success(self, crud_client, this_receiver):
        body = {"url": "https://google.ru", "method": "post", "receiver_body": {}}
        res = crud_client.patch(
            f"{self._url}/{this_receiver}",
            data=json.dumps(body),
        )
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["url"] == body["url"]
        assert res_body["receiver_body"] == body["receiver_body"]
        get = crud_client.get(f"{self._url}/{this_receiver}")
        assert get.json() == res.json()

    def test_get_by_id_not_found(self, crud_client):
        res = crud_client.get(f"{self._url}/{888}")
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_by_id_not_found(self, crud_client):
        body = {"url": "https://nf.nf", "method": "post", "receiver_body": {}}
        res = crud_client.patch(f"{self._url}/{888}", data=json.dumps(body))
        assert res.status_code == status.HTTP_404_NOT_FOUND
