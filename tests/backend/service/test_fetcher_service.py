import pytest
import sqlalchemy

from aciniformes_backend.models import Fetcher
from aciniformes_backend.routes.fetcher import CreateSchema as FetcherCreateSchema
from aciniformes_backend.serivce.fetcher import PgFetcherService


@pytest.fixture
def fetcher_schema():
    body = {
        "id": 6,
        "type_": "ping",
        "address": "https://www.python.org",
        "fetch_data": "string",
        "delay_ok": 30,
        "delay_fail": 40,
    }
    schema = FetcherCreateSchema(**body)
    return schema


@pytest.fixture()
def db_fetcher(dbsession, fetcher_schema):
    q = sqlalchemy.insert(Fetcher).values(**fetcher_schema.model_dump(exclude_unset=True)).returning(Fetcher)
    fetcher = dbsession.scalar(q)
    dbsession.flush()
    yield fetcher
    if dbsession.get(Fetcher, fetcher.id_):
        dbsession.delete(fetcher)
        dbsession.flush()


class TestFetcherService:
    @pytest.mark.asyncio
    async def test_create(self, dbsession, fetcher_schema):
        res = await PgFetcherService(dbsession).create(fetcher_schema.model_dump(exclude_unset=True))
        assert res is not None
        assert type(res) is int
        q = dbsession.scalar(sqlalchemy.select(Fetcher).where(Fetcher.id_ == res))
        assert q is not None

    @pytest.mark.asyncio
    async def test_get_all(self, dbsession, db_fetcher):
        res = await PgFetcherService(dbsession).get_all()
        assert type(res) is list
        assert type(res[0]) is Fetcher

    @pytest.mark.asyncio
    async def test_get_by_id(self, dbsession, db_fetcher):
        res = await PgFetcherService(dbsession).get_by_id(db_fetcher.id_)
        assert res.address == db_fetcher.address
        assert res.type_ == db_fetcher.type_

    @pytest.mark.asyncio
    async def test_delete(self, dbsession, db_fetcher):
        await PgFetcherService(dbsession).delete(db_fetcher.id_)

    @pytest.mark.asyncio
    async def test_update(self, dbsession, db_fetcher):
        res = await PgFetcherService(dbsession).update(db_fetcher.id_, {"type_": "post"})
        assert res.type_ == "post"
