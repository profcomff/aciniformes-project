import pytest

from aciniformes_backend.exceptions import AlreadyRunning
from aciniformes_backend.models import Fetcher, Metric


@pytest.fixture()
def fetcher_obj():
    yield Fetcher(
        **{
            "type_": "ping",
            "address": "https://www.google.com",
            "fetch_data": "string",
            "delay_ok": 30,
            "delay_fail": 40,
        }
    )


class TestSchedulerService:
    @pytest.mark.asyncio
    async def test_add_fetcher_success(self, pg_scheduler_service, fetcher_obj):
        pg_scheduler_service.add_fetcher(fetcher_obj)
        fetchers = pg_scheduler_service.get_jobs()
        assert f'{fetcher_obj.address} None' in fetchers

    @pytest.mark.asyncio
    async def test_delete_fetcher(self, pg_scheduler_service, fetcher_obj):
        pg_scheduler_service.add_fetcher(fetcher_obj)
        fetchers = pg_scheduler_service.get_jobs()
        assert f"{fetcher_obj.address} {fetcher_obj.create_ts}" in fetchers

        pg_scheduler_service.delete_fetcher(fetcher_obj)
        fetchers = pg_scheduler_service.get_jobs()
        assert fetcher_obj not in fetchers

    @pytest.mark.asyncio
    async def test_get_jobs(self, pg_scheduler_service):
        res = pg_scheduler_service.get_jobs()
        assert type(res) is list

    @pytest.mark.asyncio
    async def test_start_already_started(self, pg_scheduler_service, crud_client):
        await pg_scheduler_service.start()
        with pytest.raises(AlreadyRunning):
            await pg_scheduler_service.start()
        pg_scheduler_service.stop()

    @pytest.mark.asyncio
    async def test_ping_fail(self, pg_scheduler_service, fetcher_obj, dbsession):
        fetcher = Fetcher(
            **{
                "type_": "ping",
                "address": "fasdlj",
                "fetch_data": "string",
                "delay_ok": 30,
                "delay_fail": 40,
            }
        )
        pg_scheduler_service.add_fetcher(fetcher)
        pg_scheduler_service._fetch_it(fetcher)
        metrics = dbsession.query(Metric).all()
        for metric in metrics:
            if metric.name == fetcher.address:
                assert not metric['ok']
