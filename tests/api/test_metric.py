import json
import pytest
from starlette import status
from aciniformes_backend.settings import get_settings
from aciniformes_backend.models import Metric


class TestMetric:
    _url = "/metric"
    settings = get_settings()
