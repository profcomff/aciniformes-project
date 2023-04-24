import pytest

import ping.service.exceptions as exc
from aciniformes_backend.models import Fetcher


@pytest.fixture()
def fetcher_obj():
    yield Fetcher(
        **{
            "type_": "get_ok",
            "address": "https://www.python.org",
            "fetch_data": "string",
            "delay_ok": 30,
            "delay_fail": 40,
        }
    )


class TestSchedulerService:
    @pytest.mark.asyncio
    async def test_add_fetcher_success(
        self, pg_scheduler_service, fake_crud_service, fetcher_obj
    ):
        pg_scheduler_service.add_fetcher(fetcher_obj)

    @pytest.mark.asyncio
    async def test_delete_fetcher(
        self, pg_scheduler_service, fake_crud_service, fetcher_obj
    ):
        pg_scheduler_service.delete_fetcher(
            f"{fetcher_obj.address} {fetcher_obj.create_ts}"
        )

    @pytest.mark.asyncio
    async def test_get_jobs(self, pg_scheduler_service, fake_crud_service):
        res = await pg_scheduler_service.get_jobs()
        assert type(res) is list

    @pytest.mark.asyncio
    async def test_start_success(self, pg_scheduler_service, fake_crud_service):
        await pg_scheduler_service.start()
        assert pg_scheduler_service.scheduler['started']
        await pg_scheduler_service.stop()

    @pytest.mark.asyncio
    async def test_start_already_started(self, pg_scheduler_service, fake_crud_service):
        pass

    @pytest.mark.asyncio
    async def test_stop(self, pg_scheduler_service, fake_crud_service):
        pass

    @pytest.mark.asyncio
    async def test_stop_already_stopped(self, pg_scheduler_service, fake_crud_service):
        pass

    @pytest.mark.asyncio
    async def test_write_alert(self, pg_scheduler_service, fake_crud_service):
        pass
