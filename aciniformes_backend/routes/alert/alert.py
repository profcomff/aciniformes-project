from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Json
from fastapi import Depends
from starlette import status
from aciniformes_backend.serivce import (
    pg_alert_service,
    AlertServiceInterface,
    exceptions as exc
)


class CreateSchema(BaseModel):
    data: Json
    receiver: int
    filter: str


class UpdateSchema(BaseModel):
    data: Json | None
    receiver: int | None
    filter: str | None


class GetSchema(BaseModel):
    id: int


router = APIRouter()


@router.post("")
async def create(
        create_schema: CreateSchema,
        alert_service: AlertServiceInterface = Depends(pg_alert_service)
):
    await alert_service.create(create_schema.dict(exclude_unset=True))
    return status.HTTP_201_CREATED


@router.get("")
async def get_all(
        alert_service: AlertServiceInterface = Depends(pg_alert_service)
):
    res = await alert_service.get_all()
    return res


@router.get("/{id}")
async def get(
        id: int,
        alert_service: AlertServiceInterface = Depends(pg_alert_service)
):
    try:
        res = await alert_service.get_by_id(id)
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return res


@router.patch("/{id}")
async def update(
        id: int,
        update_schema: UpdateSchema,
        alert_service: AlertServiceInterface = Depends(pg_alert_service)
):
    res = await alert_service.update(id, update_schema.dict(exclude_unset=True))
    return res


@router.delete("/{id}")
async def delete(
        id: int,
        alert_service: AlertServiceInterface = Depends(pg_alert_service)
):
    await alert_service.delete(id)
