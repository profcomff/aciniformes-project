
import pytest
import sqlalchemy

import aciniformes_backend.serivce.exceptions as exc
from aciniformes_backend.models import Alert, Receiver
from aciniformes_backend.routes.alert.alert import CreateSchema as AlertCreateSchema
from aciniformes_backend.routes.alert.reciever import CreateSchema as ReceiverCreateSchema


@pytest.fixture
def receiver_schema():
    body = {"url": "string", "method": "post", "receiver_body": {}}
    schema = ReceiverCreateSchema(**body)
    return schema


@pytest.fixture
def db_receiver(dbsession, receiver_schema):
    q = sqlalchemy.insert(Receiver).values(**receiver_schema.dict(exclude_unset=True)).returning(Receiver)
    receiver = dbsession.execute(q).scalar()
    dbsession.flush()
    yield receiver
    if dbsession.get(Receiver, receiver.id_):
        dbsession.delete(receiver)
        dbsession.flush()


@pytest.fixture
def alert_schema(receiver_schema):
    body = {
        "data": {"type": "string", "name": "string"},
        "filter": "string",
    }
    schema = AlertCreateSchema(**body)
    return schema


@pytest.fixture
def db_alert(db_receiver, dbsession, alert_schema):
    q = sqlalchemy.insert(Alert).values(**alert_schema.dict(exclude_unset=True)).returning(Alert)
    alert = dbsession.execute(q).scalar()
    dbsession.flush()
    yield alert
    if dbsession.get(Alert, alert.id_):
        dbsession.delete(alert)
        dbsession.flush()


class TestReceiverService:
    @pytest.mark.asyncio
    async def test_create(self, pg_receiver_service, receiver_schema, dbsession):
        res = await pg_receiver_service.create(receiver_schema.dict())
        assert res is not None
        assert type(res) == int
        q = dbsession.query(Receiver).filter(Receiver.id_ == res).one_or_none()
        assert q is not None

    @pytest.mark.asyncio
    async def test_get_all(self, pg_receiver_service, db_receiver, db_alert):
        res = await pg_receiver_service.get_all()
        assert len(res)
        assert type(res) is list
        assert type(res[0]) is Receiver

    @pytest.mark.asyncio
    async def test_get_by_id(self, pg_receiver_service, db_receiver):
        res = await pg_receiver_service.get_by_id(db_receiver.id_)
        assert res is not None
        assert res.url == db_receiver.url
        with pytest.raises(exc.ObjectNotFound):
            await pg_receiver_service.get_by_id(db_receiver.id_ + 1000)

    @pytest.mark.asyncio
    async def test_delete(self, pg_receiver_service, db_receiver):
        await pg_receiver_service.delete(db_receiver.id_)

    @pytest.mark.asyncio
    async def test_update(self, pg_receiver_service, db_receiver, dbsession):
        res = await pg_receiver_service.update(db_receiver.id_, {"url": "Alex", "method": "post", "receiver_body": {}})
        assert res.url == "Alex"
        assert res.receiver_body == {}


class TestAlertService:
    @pytest.mark.asyncio
    async def test_create(self, pg_alert_service, alert_schema, db_receiver):
        res = await pg_alert_service.create(
            alert_schema.dict(exclude_unset=True),
        )
        assert type(res) == int

    @pytest.mark.asyncio
    async def test_get_all(self, pg_alert_service, db_alert):
        res = await pg_alert_service.get_all()
        assert len(res)
        assert type(res) is list
        assert type(res[0]) is Alert

    @pytest.mark.asyncio
    async def test_get_by_id(self, pg_alert_service, db_alert):
        res = await pg_alert_service.get_by_id(db_alert.id_)
        assert res is not None
        assert res.data == db_alert.data
        assert res.filter == db_alert.filter
        with pytest.raises(exc.ObjectNotFound):
            await pg_alert_service.get_by_id(db_alert.id_ + 1000)

    @pytest.mark.asyncio
    async def test_delete(self, pg_alert_service, db_alert):
        await pg_alert_service.delete(db_alert.id_)

    @pytest.mark.asyncio
    async def test_update(self, pg_alert_service, db_alert):
        res = await pg_alert_service.update(db_alert.id_, {"data": {"type": "stig", "name": "stig"}})
        assert res.data == {"type": "stig", "name": "stig"}
