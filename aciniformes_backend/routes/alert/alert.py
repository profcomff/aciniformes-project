from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from starlette import status

from aciniformes_backend.models.alerts import Receiver
from aciniformes_backend.serivce import AlertServiceInterface, alert_service
from aciniformes_backend.serivce import exceptions as exc


class CreateSchema(BaseModel):
    data: dict
    filter: str


class PostResponseSchema(CreateSchema):
    id: int | None


class UpdateSchema(BaseModel):
    data: dict | None
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
