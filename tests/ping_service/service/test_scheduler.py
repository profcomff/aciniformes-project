import pytest

from aciniformes_backend.models import Fetcher, Metric


@pytest.fixture()
def fetcher_obj():
    yield Fetcher(
        **{
            "type_": "ping",
            "address": "http://testserver",
            "fetch_data": "string",
            "delay_ok": 30,
            "delay_fail": 40,
        }
    )


class TestSchedulerService:
    @pytest.mark.asyncio
    async def test_add_fetcher_success(self, pg_scheduler_service, fake_crud_service, fetcher_obj):
        pg_scheduler_service.add_fetcher(fetcher_obj)
        fetchers = pg_scheduler_service.get_jobs()
        assert f'{fetcher_obj.address} None' in fetchers

    @pytest.mark.asyncio
    async def test_delete_fetcher(self, pg_scheduler_service, fake_crud_service, fetcher_obj):
        pg_scheduler_service.add_fetcher(fetcher_obj)
        fetchers = pg_scheduler_service.get_jobs()
        assert f"{fetcher_obj.address} {fetcher_obj.create_ts}" in fetchers

        pg_scheduler_service.delete_fetcher(fetcher_obj)
        fetchers = pg_scheduler_service.get_jobs()
        assert fetcher_obj not in fetchers

    @pytest.mark.asyncio
    async def test_get_jobs(self, pg_scheduler_service, fake_crud_service):
        res = pg_scheduler_service.get_jobs()
        assert type(res) is list

    @pytest.mark.asyncio
    async def test_start_already_started(self, pg_scheduler_service, fake_crud_service):
        pg_scheduler_service.start()
        fail = False
        try:
            pg_scheduler_service.start()
        except:
            fail = True
        assert fail

    @pytest.mark.asyncio
    async def test_ping(self, pg_scheduler_service, fetcher_obj, fake_crud_service, dbsession):
        pg_scheduler_service.add_fetcher(fetcher_obj)
        pg_scheduler_service._fetch_it(fetcher_obj)
        metrics = dbsession.query(Metric).all()
        for metric in metrics:
            if metric.name == fetcher_obj.address:
                assert metric['ok']
        fetcher = Fetcher(
            **{
                "type_": "ping",
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
