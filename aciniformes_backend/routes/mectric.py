from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from starlette import status
from fastapi_sqlalchemy import db
import sqlalchemy as sa
import aciniformes_backend.models as db_models
from aciniformes_backend.routes import exceptions as exc


class CreateSchema(BaseModel):
    name: str
    ok: bool
    time_delta: float


class ResponsePostSchema(CreateSchema):
    id: int | None = None


class GetSchema(BaseModel):
    id: int
    name: str
    ok: bool
    time_delta: float


router = APIRouter()


@router.post("", response_model=ResponsePostSchema)
async def create(
    metric_schema: CreateSchema,
    _: dict[str] = Depends(UnionAuth(['pinger.metric.create'])),
):
    """Создание метрики."""
    q = sa.insert(db_models.Metric).values(**metric_schema.model_dump()).returning(db_models.Metric)
    metric = db.session.scalar(q)
    db.session.flush()
    return ResponsePostSchema(**metric_schema.model_dump(), id=metric.id_)


@router.get("")
async def get_all(
    _: dict[str] = Depends(UnionAuth(['pinger.metric.read'])),
):
    """Получение всех метрик."""
    return list(db.session.scalars(sa.select(db_models.Fetcher)).all())


@router.get("/{id}")
async def get(
    id: int,
    _: dict[str] = Depends(UnionAuth(['pinger.metric.read'])),
):
    """Получение одной метрики по id."""
    try:
        q = sa.select(db_models.Fetcher).where(db_models.Fetcher.id_ == id)
        res = db.session.scalar(q)
        if not res:
            raise exc.ObjectNotFound(id)
        return res
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
