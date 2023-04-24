import pytest
import sqlalchemy

from aciniformes_backend.models import Fetcher
from aciniformes_backend.routes.fetcher import CreateSchema as FetcherCreateSchema


@pytest.fixture
def fetcher_schema():
    body = {
        "id": 6,
        "type_": "get",
        "address": "string",
        "fetch_data": "string",
        "delay_ok": 0,
        "delay_fail": 0,
    }
    schema = FetcherCreateSchema(**body)
    return schema


@pytest.fixture()
def db_fetcher(dbsession, fetcher_schema):
    q = (
        sqlalchemy.insert(Fetcher)
        .values(**fetcher_schema.dict(exclude_unset=True))
        .returning(Fetcher)
    )
    fetcher = dbsession.scalar(q)
    dbsession.flush()
    yield fetcher
    if dbsession.get(Fetcher, fetcher.id_):
        dbsession.delete(fetcher)
        dbsession.flush()


class TestFetcherService:
    @pytest.mark.asyncio
    async def test_create(self, pg_fetcher_service, fetcher_schema, dbsession):
        res = await pg_fetcher_service.create(fetcher_schema.dict(exclude_unset=True))
        assert res is not None
        assert type(res) is int
        q = dbsession.scalar(sqlalchemy.select(Fetcher).where(Fetcher.id_ == res))
        assert q is not None

    @pytest.mark.asyncio
    async def test_get_all(self, pg_fetcher_service, db_fetcher):
        res = await pg_fetcher_service.get_all()
        assert type(res) is list
        assert type(res[0]) is Fetcher

    @pytest.mark.asyncio
    async def test_get_by_id(self, pg_fetcher_service, db_fetcher):
        res = await pg_fetcher_service.get_by_id(db_fetcher.id_)
        assert res.address == db_fetcher.address
        assert res.type_ == db_fetcher.type_

    @pytest.mark.asyncio
    async def test_delete(self, pg_fetcher_service, db_fetcher):
        await pg_fetcher_service.delete(db_fetcher.id_)

    @pytest.mark.asyncio
    async def test_update(self, pg_fetcher_service, db_fetcher):
        res = await pg_fetcher_service.update(db_fetcher.id_, {"type_": "post"})
        assert res.type_ == "post"
