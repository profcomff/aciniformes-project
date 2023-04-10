import pytest
import sqlalchemy

import aciniformes_backend.serivce.exceptions as exc
from aciniformes_backend.models import Metric
from aciniformes_backend.routes.mectric import \
    CreateSchema as MetricCreateSchema


@pytest.fixture
def metric_schema():
    body = {"id": 44, "metrics": {}}
    schema = MetricCreateSchema(**body)
    return schema


@pytest.fixture()
def db_metric(dbsession, metric_schema):
    q = (
        sqlalchemy.insert(Metric)
        .values(**metric_schema.dict(exclude_unset=True))
        .returning(Metric)
    )
    metric = dbsession.scalar(q)
    dbsession.flush()
    yield metric
    if dbsession.get(Metric, metric.id_):
        dbsession.delete(metric)
        dbsession.flush()


class TestMetricService:
    @pytest.mark.asyncio
    async def test_create(self, pg_metric_service, metric_schema, dbsession):
        res = await pg_metric_service.create(metric_schema.dict(exclude_unset=True))
        assert res is not None
        assert type(res) is int
        q = dbsession.scalar(sqlalchemy.select(Metric).where(Metric.id_ == res))
        assert q is not None

    @pytest.mark.asyncio
    async def test_get_all(self, pg_metric_service):
        res = await pg_metric_service.get_all()
        assert type(res) is list
        assert type(res[0]) is Metric

    @pytest.mark.asyncio
    async def test_get_by_id(self, pg_metric_service, db_metric):
        res = await pg_metric_service.get_by_id(db_metric.id_)
        assert res.metrics == db_metric.metrics
