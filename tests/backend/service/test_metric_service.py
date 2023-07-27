import pytest
import sqlalchemy

from aciniformes_backend.models import Metric
from aciniformes_backend.routes.mectric import CreateSchema as MetricCreateSchema
from aciniformes_backend.serivce.metric import PgMetricService


@pytest.fixture
def metric_schema():
    body = {"id": 44, "name": "string", "ok": True, "time_delta": 0}
    schema = MetricCreateSchema(**body)
    return schema


@pytest.fixture()
def db_metric(dbsession, metric_schema):
    q = sqlalchemy.insert(Metric).values(**metric_schema.dict(exclude_unset=True)).returning(Metric)
    metric = dbsession.scalar(q)
    dbsession.flush()
    yield metric
    if dbsession.get(Metric, metric.id_):
        dbsession.delete(metric)
        dbsession.flush()


class TestMetricService:
    @pytest.mark.asyncio
    async def test_create(self, metric_schema, dbsession):
        res = await PgMetricService(dbsession).create(metric_schema.model_dump(exclude_unset=True))
        assert res is not None
        assert type(res) is int
        q = dbsession.scalar(sqlalchemy.select(Metric).where(Metric.id_ == res))
        assert q is not None

    @pytest.mark.asyncio
    async def test_get_all(self, dbsession):
        res = await PgMetricService(dbsession).get_all()
        assert type(res) is list
        assert type(res[0]) is Metric

    @pytest.mark.asyncio
    async def test_get_by_id(self, dbsession, db_metric):
        res = await PgMetricService(dbsession).get_by_id(db_metric.id_)
        assert res.name == db_metric.name
        assert res.ok == db_metric.ok
