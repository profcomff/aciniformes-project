import json
import pytest
from starlette import status
from aciniformes_backend.settings import get_settings
from aciniformes_backend.models import Fetcher
from aciniformes_backend.serivce import fetcher_service


def test_fake_service(service_config):
    s = fetcher_service()
    assert s.session is None
    assert type(s.repository) is dict


class TestFetcher:
    _url = "/fetcher"
    settings = get_settings()
