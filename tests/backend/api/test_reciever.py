import json

import pytest
import pytest_asyncio
import sqlalchemy as sa
from fastapi_sqlalchemy import db
from starlette import status

import aciniformes_backend.models as db_models


receiver = {"url": "https://google.com", "method": "post", "receiver_body": {}}


@pytest_asyncio.fixture
async def this_receiver(dbsession):
    global receiver
    q = sa.insert(db_models.Receiver).values(**receiver).returning(db_models.Receiver)
    receiver_db = dbsession.execute(q).scalar()
    dbsession.flush()

    yield receiver_db.id_

    q = sa.delete(db_models.Receiver).where(db_models.Receiver.id_ == id)
    dbsession.execute(q)
    dbsession.flush()


@pytest.mark.authenticated("pinger.receiver.create")
def test_post_success(crud_client):
    body = {"url": "https://google.com", "method": "post", "receiver_body": {}}
    res = crud_client.post("/receiver", json=body)
    assert res.status_code == status.HTTP_200_OK
    res_body = res.json()
    assert res_body["url"] == body["url"]
    assert res_body["receiver_body"] == body["receiver_body"]


@pytest.mark.authenticated("pinger.receiver.read")
def test_get_by_id_success(crud_client, this_receiver):
    global receiver
    res = crud_client.get(f"/receiver/{this_receiver}")
    assert res.status_code == status.HTTP_200_OK
    res_body = res.json()
    assert res_body["url"] == receiver["url"]
    assert res_body["receiver_body"] == receiver["receiver_body"]


@pytest.mark.authenticated("pinger.receiver.read", "pinger.receiver.delete")
def test_delete_by_id_success(crud_client, this_receiver):
    res = crud_client.delete(f"/receiver/{this_receiver}")
    assert res.status_code == status.HTTP_200_OK
    res = crud_client.get(f"/receiver/{this_receiver}")
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.authenticated("pinger.receiver.read")
def test_get_success(crud_client, this_receiver):
    res = crud_client.get("/receiver")
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json())
    get = crud_client.get(f"/receiver/{this_receiver}")
    assert get.json() in res.json()


@pytest.mark.authenticated("pinger.receiver.read", "pinger.receiver.update")
def test_patch_by_id_success(crud_client, this_receiver):
    body = {"url": "https://google.ru", "method": "post", "receiver_body": {}}
    res = crud_client.patch(
        f"/receiver/{this_receiver}",
        data=json.dumps(body),
    )
    assert res.status_code == status.HTTP_200_OK
    res_body = res.json()
    assert res_body["url"] == body["url"]
    assert res_body["receiver_body"] == body["receiver_body"]
    get = crud_client.get(f"/receiver/{this_receiver}")
    assert get.json() == res.json()


@pytest.mark.authenticated("pinger.receiver.read")
def test_get_by_id_not_found(crud_client):
    res = crud_client.get(f"/receiver/{888}")
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.authenticated("pinger.receiver.update")
def test_patch_by_id_not_found(crud_client):
    body = {"url": "https://nf.nf", "method": "post", "receiver_body": {}}
    res = crud_client.patch(f"/receiver/{888}", data=json.dumps(body))
    assert res.status_code == status.HTTP_404_NOT_FOUND
