import json
import pytest
from starlette import status
from aciniformes_backend.settings import get_settings
from aciniformes_backend.models import Alert, Receiver
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
        assert self.s.repository[this_alert["id"]]["data"] == body["data"]

    def test_get_by_id_not_found(self, client):
        pass

    def test_delete_by_id_not_found(self, client):
        pass

    def test_patch_by_id_not_found(self, client):
        pass


class TestReceiver:
    _url = "/receiver"
    settings = get_settings()
    Config.fake = True
    s = receiver_service()

    def test_post_success(self, client):
        pass

    def test_get_by_id_success(self, client):
        pass

    def test_delete_by_id_success(self, client):
        pass

    def test_get_success(self, client):
        pass

    def test_patch_by_id_success(self, client):
        pass

    def test_get_by_id_not_found(self, client):
        pass

    def test_delete_by_id_not_found(self, client):
        pass

    def test_patch_by_id_not_found(self, client):
        pass
