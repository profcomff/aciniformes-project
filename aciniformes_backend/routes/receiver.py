import logging
from enum import Enum

import sqlalchemy as sa
from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi_sqlalchemy import db
from pydantic import BaseModel
from starlette import status

import aciniformes_backend.models as db_models
from aciniformes_backend.routes import exceptions as exc


logger = logging.getLogger(__name__)


class Method(str, Enum):
    POST: str = "post"
    GET: str = "get"


class CreateSchema(BaseModel):
    url: str
    method: Method
    receiver_body: dict[str, str | int | list]


class PostResponseSchema(CreateSchema):
    url: str | None = None
    method: Method
    receiver_body: dict[str, str | int | list] | None = None


class UpdateSchema(BaseModel):
    url: str | None
    method: Method | None
    receiver_body: dict[str, str | int | list] | None = None


class GetSchema(BaseModel):
    url: str
    method: Method
    receiver_body: dict[str, str | int | list] | None = None


router = APIRouter()


@router.post("", response_model=PostResponseSchema)
async def create(
    create_schema: CreateSchema,
    _: dict[str] = Depends(UnionAuth(['pinger.receiver.create'])),
):
    """Создание получателя уведомлений."""
    q = sa.insert(db_models.Receiver).values(**create_schema.model_dump()).returning(db_models.Receiver)
    receiver = db.session.execute(q).scalar()
    db.session.flush()
    return PostResponseSchema(**create_schema.model_dump(), id=receiver.id_)


@router.get("")
async def get_all(
    _: dict[str] = Depends(UnionAuth(['pinger.receiver.read'])),
):
    """Получить всех получателей уведомлений."""
    return list(db.session.scalars(sa.select(db_models.Receiver)).all())


@router.get("/{id}")
async def get(
    id: int,
    _: dict[str] = Depends(UnionAuth(['pinger.receiver.read'])),
):
    """Получение получателя уведомлений."""
    try:
        q = sa.select(db_models.Receiver).where(db_models.Receiver.id_ == id)
        res = db.session.scalar(q)
        if not res:
            raise exc.ObjectNotFound(id)
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.patch("/{id}")
async def update(
    id: int,
    update_schema: UpdateSchema,
    _: dict[str] = Depends(UnionAuth(['pinger.receiver.update'])),
):
    """Обновление получателя уведомлений по id."""
    try:
        q = sa.select(db_models.Receiver).where(db_models.Receiver.id_ == id)
        res = db.session.scalar(q)
        if not res:
            raise exc.ObjectNotFound(id)
        q = (
            sa.update(db_models.Receiver)
            .where(db_models.Receiver.id_ == id)
            .values(**update_schema.model_dump())
            .returning(db_models.Receiver)
        )
        res = db.session.execute(q).scalar()
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return res


@router.delete("/{id}")
async def delete(
    id: int,
    _: dict[str] = Depends(UnionAuth(['pinger.receiver.delete'])),
):
    """Удаление получателя уведомлений по id."""
    q = sa.delete(db_models.Receiver).where(db_models.Receiver.id_ == id)
    db.session.execute(q)
    db.session.flush()
