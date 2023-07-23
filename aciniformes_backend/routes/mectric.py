from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from starlette import status

from aciniformes_backend.serivce import MetricServiceInterface
from aciniformes_backend.serivce import exceptions as exc
from aciniformes_backend.serivce import metric_service


class CreateSchema(BaseModel):
    name: str
    ok: bool
    time_delta: float


class ResponsePostSchema(CreateSchema):
    id: int | None


class GetSchema(BaseModel):
    id: int
    name: str
    ok: bool
    time_delta: float


router = APIRouter()


@router.post("", response_model=ResponsePostSchema)
async def create(
    metric_schema: CreateSchema,
    metric: MetricServiceInterface = Depends(metric_service),
):
    id_ = await metric.create(metric_schema.dict())
    return ResponsePostSchema(**metric_schema.dict(), id=id_)


@router.get("")
async def get_all(metric: MetricServiceInterface = Depends(metric_service)):
    res = await metric.get_all()
    return res


@router.get("/{id}")
async def get(id: int, metric: MetricServiceInterface = Depends(metric_service)):
    try:
        res = await metric.get_by_id(id)
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return res
