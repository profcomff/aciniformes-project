import json
import pytest
from starlette import status
from aciniformes_backend.settings import get_settings
from aciniformes_backend.models import Metric
from aciniformes_backend.serivce import metric_service, Config


class TestMetric:
    _url = "/metric"
    settings = get_settings()
    Config.fake = True
    s = metric_service()

    def test_post_success(self, client):
        pass

    def test_get_by_id_success(self, client):
        pass

    def test_get_success(self, client):
        pass

    def test_get_by_id_not_found(self, client):
        pass
