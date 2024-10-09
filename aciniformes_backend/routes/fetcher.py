import logging

import sqlalchemy as sa
from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi_sqlalchemy import db
from pydantic import BaseModel, HttpUrl
from pydantic.functional_serializers import PlainSerializer
from starlette import status
from typing_extensions import Annotated

import aciniformes_backend.models as db_models
from aciniformes_backend.models.fetcher import FetcherType
from aciniformes_backend.routes import exceptions as exc


logger = logging.getLogger(__name__)
router = APIRouter()


class CreateSchema(BaseModel):
    type_: FetcherType
    address: str
    fetch_data: str
    delay_ok: int
    delay_fail: int


class ResponsePostSchema(CreateSchema):
    id: int | None = None


class UpdateSchema(BaseModel):
    type_: FetcherType | None = None
    address: Annotated[HttpUrl, PlainSerializer(lambda x: str(x), return_type=str)] | None = None
    fetch_data: str | None = None
    delay_ok: int | None = None
    delay_fail: int | None = None


class GetSchema(BaseModel):
    id: int


@router.post("", response_model=ResponsePostSchema)
async def create(
    create_schema: CreateSchema,
    _: dict[str] = Depends(UnionAuth(['pinger.fetcher.create'])),
):
    """
    Создает новый сборщик метрик.
    """
    q = sa.insert(db_models.Fetcher).values(**create_schema.model_dump()).returning(db_models.Fetcher)
    fetcher = db.session.scalar(q)
    db.session.flush()
    return ResponsePostSchema(**create_schema.model_dump(), id=fetcher.id_)


@router.get("")
async def get_all(
    _: dict[str] = Depends(UnionAuth(['pinger.fetcher.read'])),
):
    """
    Возвращает все сборщики метрик.
    """
    return list(db.session.scalars(sa.select(db_models.Fetcher)).all())


@router.get("/{id}")
async def get(
    id: int,
    _: dict[str] = Depends(UnionAuth(['pinger.fetcher.read'])),
):
    """Получение одного сборщика метрик по id"""
    try:
        q = sa.select(db_models.Fetcher).where(db_models.Fetcher.id_ == id)
        res = db.session.scalar(q)
        if not res:
            raise exc.ObjectNotFound(id)
        return res
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.patch("/{id}")
async def update(
    id: int,
    update_schema: UpdateSchema,
    _: dict[str] = Depends(UnionAuth(['pinger.fetcher.update'])),
):
    """Обновление одного сборщика метрик по id"""
    try:
        q = (
            sa.update(db_models.Fetcher)
            .where(db_models.Fetcher.id_ == id)
            .values(**update_schema)
            .returning(db_models.Fetcher)
        )
        if not await db.get_by_id(id):
            raise exc.ObjectNotFound(id)
        res = db.session.execute(q).scalar()
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return res


@router.delete("/{id}")
async def delete(
    id: int,
    _: dict[str] = Depends(UnionAuth(['pinger.fetcher.delete'])),
):
    """Удаление одного сборщика метрик по id"""
    q = sa.delete(db_models.Fetcher).where(db_models.Fetcher.id_ == id)
    db.session.execute(q)
    db.session.flush()
