import json
import pytest
from starlette import status
from aciniformes_backend.settings import get_settings
from aciniformes_backend.models import Fetcher
from aciniformes_backend.serivce import fetcher_service, Config


def test_fake_service(fake_config):
    s = fetcher_service()
    assert s.session is None
    assert type(s.repository) is dict


class TestFetcher:
    _url = "/fetcher"
    settings = get_settings()
    Config.fake = True
    s = fetcher_service()

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

    def test_patch_by_id_not_found(self, client):
        pass
