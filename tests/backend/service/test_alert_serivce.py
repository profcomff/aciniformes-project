import pytest
import sqlalchemy

import aciniformes_backend.serivce.exceptions as exc
from aciniformes_backend.models import Alert, Receiver
from aciniformes_backend.routes.alert import CreateSchema as AlertCreateSchema
from aciniformes_backend.routes.reciever import CreateSchema as ReceiverCreateSchema
from aciniformes_backend.serivce.alert import PgAlertService
from aciniformes_backend.serivce.receiver import PgReceiverService


@pytest.fixture
def receiver_schema():
    body = {"url": "https://google.com", "method": "post", "receiver_body": {}}
    schema = ReceiverCreateSchema(**body)
    return schema


@pytest.fixture
def db_receiver(dbsession, receiver_schema):
    q = sqlalchemy.insert(Receiver).values(**receiver_schema.model_dump(exclude_unset=True)).returning(Receiver)
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
    q = sqlalchemy.insert(Alert).values(**alert_schema.model_dump(exclude_unset=True)).returning(Alert)
    alert = dbsession.execute(q).scalar()
    dbsession.flush()
    yield alert
    if dbsession.get(Alert, alert.id_):
        dbsession.delete(alert)
        dbsession.flush()


class TestReceiverService:
    @pytest.mark.asyncio
    async def test_create(self, receiver_schema, dbsession):
        res = await PgReceiverService(dbsession).create(item=receiver_schema.model_dump())
        assert res is not None
        assert type(res) == int
        q = dbsession.query(Receiver).filter(Receiver.id_ == res).one_or_none()
        assert q is not None

    @pytest.mark.asyncio
    async def test_get_all(self, db_receiver, dbsession):
        res = await PgReceiverService(dbsession).get_all()
        assert len(res)
        assert type(res) is list
        assert type(res[0]) is Receiver

    @pytest.mark.asyncio
    async def test_get_by_id(self, db_receiver, dbsession):
        res = await PgReceiverService(dbsession).get_by_id(db_receiver.id_)
        assert res is not None
        assert res.url == db_receiver.url
        with pytest.raises(exc.ObjectNotFound):
            await PgReceiverService(dbsession).get_by_id(db_receiver.id_ + 1000)

    @pytest.mark.asyncio
    async def test_delete(self, db_receiver, dbsession):
        await PgReceiverService(dbsession).delete(db_receiver.id_)

    @pytest.mark.asyncio
    async def test_update(self, db_receiver, dbsession):
        res = await PgReceiverService(dbsession).update(
            db_receiver.id_, {"url": "Alex", "method": "post", "receiver_body": {}}
        )
        assert res.url == "Alex"
        assert res.receiver_body == {}


class TestAlertService:
    @pytest.mark.asyncio
    async def test_create(self, alert_schema, db_receiver, dbsession):
        res = await PgAlertService(dbsession).create(
            alert_schema.model_dump(exclude_unset=True),
        )
        assert type(res) == int

    @pytest.mark.asyncio
    async def test_get_all(self, db_alert, dbsession):
        res = await PgAlertService(dbsession).get_all()
        assert len(res)
        assert type(res) is list
        assert type(res[0]) is Alert

    @pytest.mark.asyncio
    async def test_get_by_id(self, dbsession, db_alert):
        res = await PgAlertService(dbsession).get_by_id(db_alert.id_)
        assert res is not None
        assert res.data == db_alert.data
        assert res.filter == db_alert.filter
        with pytest.raises(exc.ObjectNotFound):
            await PgAlertService(dbsession).get_by_id(db_alert.id_ + 1000)

    @pytest.mark.asyncio
    async def test_delete(self, dbsession, db_alert):
        await PgAlertService(dbsession).delete(db_alert.id_)

    @pytest.mark.asyncio
    async def test_update(self, dbsession, db_alert):
        res = await PgAlertService(dbsession).update(db_alert.id_, {"data": {"type": "stig", "name": "stig"}})
        assert res.data == {"type": "stig", "name": "stig"}
