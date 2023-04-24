import json

import pytest
from starlette import status

from aciniformes_backend.serivce import Config, alert_service, receiver_service
from aciniformes_backend.settings import get_settings


def test_fake_service(fake_config):
    s1 = alert_service()
    s2 = receiver_service()
    assert s1.session is None
    assert s2.session is None
    assert type(s1.repository) is dict
    assert type(s2.repository) is dict


@pytest.fixture
def this_alert():
    body = {
        "id": 666,
        "data": {"type": "string", "name": "string"},
        "filter": "string",
    }
    alert_service().repository[666] = body
    return body


class TestAlert:
    _url = "/alert"
    settings = get_settings()
    Config.fake = True
    s = alert_service()

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
        body = this_alert
        res = client.get(f"{self._url}/{body['id']}")
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["data"] == body["data"]
        assert res_body["filter"] == body["filter"]

    def test_delete_by_id_success(self, client, this_alert):
        res = client.delete(f"{self._url}/{this_alert['id']}")
        assert res.status_code == status.HTTP_200_OK
        assert self.s.repository[666] is None

    def test_get_success(self, client, this_alert):
        res = client.get(self._url)
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert len(res_body)

    def test_patch_by_id_success(self, client, this_alert):
        body = {
            "data": {"type": "g", "name": "s"},
        }
        res = client.patch(f"{self._url}/{this_alert['id']}", data=json.dumps(body))
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["data"] == body["data"]
        assert self.s.repository[this_alert["id"]].data == body["data"]

    def test_get_by_id_not_found(self, client, this_alert):
        res = client.get(f"{self._url}/{888}")
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_by_id_not_found(self, client, this_alert):
        body = {
            "data": {},
        }
        res = client.patch(f"{self._url}/{888}", data=json.dumps(body))
        assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.fixture
def this_receiver():
    body = {
          "id": 4,
          "url": "string",
          "method": "post",
          "receiver_body": {}
        }
    receiver_service().repository[body["id"]] = body
    return body


class TestReceiver:
    _url = "/receiver"
    Config.fake = True
    s = receiver_service()

    def test_post_success(self, client):
        body = {
              "url": "string",
              "method": "post",
              "receiver_body": {}
            }
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
        body = {
              "url": "sdasd",
              "method": "post",
              "receiver_body": {}
            }
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
        body = {"name": "st", "chat_id": 0}
        res = client.patch(f"{self._url}/{888}", data=json.dumps(body))
        assert res.status_code == status.HTTP_404_NOT_FOUND
