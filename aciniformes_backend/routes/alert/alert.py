from __future__ import annotations

import logging

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from starlette import status

from aciniformes_backend.serivce import AlertServiceInterface, alert_service
from aciniformes_backend.serivce import exceptions as exc


logger = logging.getLogger(__name__)


class CreateSchema(BaseModel):
    data: dict[str, str | list | dict | bool | int | float]
    filter: str


class PostResponseSchema(CreateSchema):
    id: int | None = None


class UpdateSchema(BaseModel):
    data: dict[str, str | list | dict] | None = None
    filter: str | None = None


class GetSchema(BaseModel):
    id: int


router = APIRouter()


@router.post("")
async def create(
    create_schema: CreateSchema,
    alert: AlertServiceInterface = Depends(alert_service),
    _: dict[str] = Depends(UnionAuth(['pinger.alert.create'])),
) -> PostResponseSchema:
    id_ = await alert.create(create_schema.model_dump(exclude_unset=True))
    return PostResponseSchema(**create_schema.model_dump(), id=id_)


@router.get("")
async def get_all(
    alert: AlertServiceInterface = Depends(alert_service),
    _: dict[str] = Depends(UnionAuth(['pinger.alert.read'])),
):
    res = await alert.get_all()
    return res


@router.get("/{id}")
async def get(
    id: int,
    alert: AlertServiceInterface = Depends(alert_service),
    _: dict[str] = Depends(UnionAuth(['pinger.alert.read'])),
):
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
    _: dict[str] = Depends(UnionAuth(['pinger.alert.update'])),
):
    try:
        res = await alert.update(id, update_schema.model_dump(exclude_unset=True))
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return res


@router.delete("/{id}")
async def delete(
    id: int,
    alert: AlertServiceInterface = Depends(alert_service),
    _: dict[str] = Depends(UnionAuth(['pinger.alert.delete'])),
):
    await alert.delete(id)
