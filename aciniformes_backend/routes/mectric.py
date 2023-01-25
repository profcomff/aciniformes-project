from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette import status
from pydantic import BaseModel, Json
from aciniformes_backend.serivce import (
    MetricServiceInterface,
    pg_metric_service,
    exceptions as exc
)


class CreateSchema(BaseModel):
    metrics: Json


class GetSchema(BaseModel):
    id: int


router = APIRouter()


@router.post("")
async def create(
        metric_schema: CreateSchema,
        metric_servie: MetricServiceInterface = Depends(pg_metric_service),
):
    await metric_servie.create(metric_schema.metrics)
    return status.HTTP_201_CREATED


@router.get("")
async def get_all(
        metric_service: MetricServiceInterface = Depends(pg_metric_service)
):
    res = await metric_service.get_all()
    return res


@router.get("/{id}")
async def get(
        id_: int,
        metric_service: MetricServiceInterface = Depends(pg_metric_service())
):
    try:
        res = await metric_service.get_by_id(id_)
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return res
