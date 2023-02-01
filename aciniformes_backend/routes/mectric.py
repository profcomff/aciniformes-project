from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette import status
from pydantic import BaseModel, Json
from typing import Any
from aciniformes_backend.serivce import (
    MetricServiceInterface,
    metric_service,
    exceptions as exc,
)


class CreateSchema(BaseModel):
    metrics: dict[str, int | str | list]


class ResponsePostSchema(CreateSchema):
    id: int | None


class GetSchema(BaseModel):
    id: int


router = APIRouter()


@router.post("", response_model=ResponsePostSchema)
async def create(
    metric_schema: CreateSchema,
    metric: MetricServiceInterface = Depends(metric_service),
):
    id_ = await metric.create(metric_schema.metrics)
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
