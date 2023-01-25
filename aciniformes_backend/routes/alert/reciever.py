from fastapi import APIRouter, Depends
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
from starlette import status
from aciniformes_backend.serivce import (
    pg_receiver_service,
    ReceiverServiceInterface,
    exceptions as exc
)


class CreateSchema(BaseModel):
    name: str
    chat_id: int


class UpdateSchema(BaseModel):
    name: str | None
    chat_id: int | None

class GetSchema(BaseModel):
    id: int


router = APIRouter()


@router.post("")
async def create(
        create_schema: CreateSchema,
        receiver_service: ReceiverServiceInterface = Depends(pg_receiver_service)
):
    await receiver_service.create(create_schema.dict())
    return status.HTTP_201_CREATED


@router.get("")
async def get_all(
        receiver_service: ReceiverServiceInterface = Depends(pg_receiver_service)
):
    res = await receiver_service.get_all()
    return res


@router.get("/{id}")
async def get(
        id: int,
        receiver_service: ReceiverServiceInterface = Depends(pg_receiver_service)
):
    try:
        res = await receiver_service.get_by_id(id)
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.patch("/{id}")
async def update(
        id: int,
        update_schema: UpdateSchema,
        receiver_service: ReceiverServiceInterface = Depends(pg_receiver_service)
):
    try:
        res = await receiver_service.update(id, update_schema.dict(exclude_unset=True))
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return res


@router.delete("/{id}")
async def delete(
        id: int,
        receiver_service: ReceiverServiceInterface = Depends(pg_receiver_service)
):
    await receiver_service.delete(id)
