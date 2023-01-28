import json
import pytest
from aciniformes_backend.routes.alert.alert import CreateSchema
from aciniformes_backend.models import Alert


@pytest.fixture
def alert_schema():
    body = {
        "data": {"type": "string", "name": "string"},
        "receiver": 0,
        "filter": "string",
    }
    schema = CreateSchema(**body)
    return schema


class TestAlertService:
    @pytest.mark.asyncio
    async def test_create(self, pg_alert_service, alert_schema):
        res = await pg_alert_service.create(alert_schema.dict(exclude_unset=True))
        assert type(res) == int

    @pytest.mark.asyncio
    async def test_get_all(self, pg_alert_service):
        pass

    @pytest.mark.asyncio
    async def test_get_by_id(self, pg_alert_service):
        pass

    @pytest.mark.asyncio
    async def test_delete(self, pg_alert_service):
        pass

    @pytest.mark.asyncio
    async def test_update(self, pg_alert_service):
        pass
