import logging
import os
import sys

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from starlette import status


sys.path.append(os.path.realpath('..'))

from service_backend import AlertServiceInterface, alert_service
from service_backend import exceptions as exc


logger = logging.getLogger(__name__)


class CreateSchema(BaseModel):
    data: dict[str, str | list | dict]
    filter: str


class PostResponseSchema(CreateSchema):
    id: int | None


class UpdateSchema(BaseModel):
    data: dict[str, str | list | dict] | None
    filter: str | None


class GetSchema(BaseModel):
    id: int


router = APIRouter()


@router.post(
    "",
    response_model=PostResponseSchema,
)
async def create(
    create_schema: CreateSchema,
    alert: AlertServiceInterface = Depends(alert_service),
):
    id_ = await alert.create(create_schema.dict(exclude_unset=True))
    return PostResponseSchema(**create_schema.dict(), id=id_)


@router.get("")
async def get_all(alert: AlertServiceInterface = Depends(alert_service)):
    res = await alert.get_all()
    return res


@router.get("/{id}")
async def get(id: int, alert: AlertServiceInterface = Depends(alert_service)):
    try:
        res = await alert.get_by_id(id)
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return res


@router.patch("/{id}")
async def update(
    id: int,
    update_schema: UpdateSchema,
    alert: AlertServiceInterface = Depends(alert_service),
):
    try:
        res = await alert.update(id, update_schema.dict(exclude_unset=True))
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return res


@router.delete("/{id}")
async def delete(
    id: int,
    alert: AlertServiceInterface = Depends(alert_service),
):
    await alert.delete(id)
