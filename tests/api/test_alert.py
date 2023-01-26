import json
import pytest
from starlette import status
from aciniformes_backend.settings import get_settings
from aciniformes_backend.models import Alert, Receiver
from aciniformes_backend.serivce import alert_service, receiver_service


def test_fake_service(service_config):
    s1 = alert_service()
    s2 = receiver_service()
    assert s1.session is None
    assert s2.session is None
    assert type(s1.repository) is dict
    assert type(s2.repository) is dict


class TestAlert:
    _url = "/alert"
    settings = get_settings()
    s = alert_service()

    def test_post_success(self, client):
        pass

    def test_get_by_id_success(self, client):
        pass

    def test_delete_by_id_success(self, client):
        pass

    def test_get_success(self):
        pass


class TestReceiver:
    _url = "/receiver"
    settings = get_settings()
