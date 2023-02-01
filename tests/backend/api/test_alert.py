import json
import pytest
from starlette import status
from aciniformes_backend.settings import get_settings
from aciniformes_backend.serivce import alert_service, receiver_service, Config


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
        "receiver": 0,
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
            "receiver": 0,
            "filter": "string",
        }
        res = client.post(self._url, data=json.dumps(body))
        res_body = res.json()
        assert res.status_code == status.HTTP_200_OK
        assert res_body["data"] == body["data"]
        assert res_body["id"] is not None
        assert res_body["filter"] == body["filter"]
        assert res_body["receiver"] == body["receiver"]

    def test_get_by_id_success(self, client, this_alert):
        body = this_alert
        res = client.get(f"{self._url}/{body['id']}")
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["data"] == body["data"]
        assert res_body["receiver"] == body["receiver"]
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
    body = {"id": 66, "name": "string", "chat_id": 0}
    receiver_service().repository[body["id"]] = body
    return body


class TestReceiver:
    _url = "/receiver"
    Config.fake = True
    s = receiver_service()

    def test_post_success(self, client, auth_header):
        body = {"name": "string", "chat_id": 0}
        res = client.post(self._url, data=json.dumps(body), headers=auth_header)
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["name"] == body["name"]
        assert res_body["id"] is not None
        assert res_body["chat_id"] == body["chat_id"]

    def test_get_by_id_success(self, client, this_receiver):
        res = client.get(f"{self._url}/{this_receiver['id']}")
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["name"] == this_receiver["name"]
        assert res_body["chat_id"] == this_receiver["chat_id"]

    def test_delete_by_id_success(self, client, this_receiver, auth_header):
        res = client.delete(f"{self._url}/{this_receiver['id']}", headers=auth_header)
        assert res.status_code == status.HTTP_200_OK
        assert self.s.repository[this_receiver["id"]] is None

    def test_get_success(self, client, this_receiver):
        res = client.get(self._url)
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json())

    def test_patch_by_id_success(self, client, this_receiver, auth_header):
        body = {"name": "s", "chat_id": 11}
        res = client.patch(f"{self._url}/{this_receiver['id']}", data=json.dumps(body), headers=auth_header)
        assert res.status_code == status.HTTP_200_OK
        res_body = res.json()
        assert res_body["name"] == body["name"]
        assert res_body["chat_id"] == body["chat_id"]

    def test_get_by_id_not_found(self, client):
        res = client.get(f"{self._url}/{888}")
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_by_id_not_found(self, client, auth_header):
        body = {"name": "st", "chat_id": 0}
        res = client.patch(f"{self._url}/{888}", data=json.dumps(body), headers=auth_header)
        assert res.status_code == status.HTTP_404_NOT_FOUND
