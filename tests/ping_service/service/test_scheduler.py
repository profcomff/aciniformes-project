import pytest
import httpx
import ping.service.exceptions as exc
from aciniformes_backend.models import Fetcher, Metric
from ping.settings import get_settings


@pytest.fixture()
def fetcher_obj():
    yield Fetcher(
        **{
            "type_": "ping",
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
        await pg_scheduler_service.add_fetcher(fetcher_obj)
        fetchers = await pg_scheduler_service.get_jobs()
        assert f'{fetcher_obj.address} None' in fetchers

    @pytest.mark.asyncio
    async def test_delete_fetcher(
        self, pg_scheduler_service, fake_crud_service, fetcher_obj
    ):
        pg_scheduler_service.delete_fetcher(
            f"{fetcher_obj.address} {fetcher_obj.create_ts}"
        )
        fetchers = await pg_scheduler_service.get_jobs()
        assert fetcher_obj not in fetchers

    @pytest.mark.asyncio
    async def test_get_jobs(self, pg_scheduler_service, fake_crud_service):
        res = await pg_scheduler_service.get_jobs()
        assert type(res) is list

    @pytest.mark.asyncio
    async def test_start_already_started(self, pg_scheduler_service, fake_crud_service):
        fail = False
        try:
            await pg_scheduler_service.start()
        except:
            fail = True
        assert fail

    @pytest.mark.asyncio
    async def test_ping(self, pg_scheduler_service, fake_crud_service, dbsession):
        fetcher = Fetcher(**{
            "type_": "get_ok",
            "address": "https://www.python.org",
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
                assert metric['ok']
        fetcher = Fetcher(**{
            "type_": "get_ok",
            "address": "https://www.ayyylmaorofl.org",
            "fetch_data": "string",
            "delay_ok": 30,
            "delay_fail": 40,
            }
        )
        pg_scheduler_service.add_fetcher(fetcher)
        pg_scheduler_service._fetch_it(fetcher)
        metrics = dbsession.query(Metric).all()
        for metric in metrics:
            if metric['name'] == fetcher.address:
                assert not metric['ok']