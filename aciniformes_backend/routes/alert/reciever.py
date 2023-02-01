from fastapi import APIRouter, Depends
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
from starlette import status
from aciniformes_backend.routes.auth import get_current_user
from aciniformes_backend.serivce import (
    receiver_service,
    ReceiverServiceInterface,
    exceptions as exc,
)


class CreateSchema(BaseModel):
    name: str
    chat_id: int


class PostResponseSchema(CreateSchema):
    id: int | None


class UpdateSchema(BaseModel):
    name: str | None
    chat_id: int | None


class GetSchema(BaseModel):
    id: int


router = APIRouter()


@router.post("", response_model=PostResponseSchema)
async def create(
    create_schema: CreateSchema,
    receiver: ReceiverServiceInterface = Depends(receiver_service),
    token=Depends(get_current_user),
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    id_ = await receiver.create(create_schema.dict())
    return PostResponseSchema(**create_schema.dict(), id=id_)


@router.get("")
async def get_all(
    receiver: ReceiverServiceInterface = Depends(receiver_service),
):
    res = await receiver.get_all()
    return res


@router.get("/{id}")
async def get(id: int, receiver: ReceiverServiceInterface = Depends(receiver_service)):
    try:
        res = await receiver.get_by_id(id)
        return res
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.patch("/{id}")
async def update(
    id: int,
    update_schema: UpdateSchema,
    receiver: ReceiverServiceInterface = Depends(receiver_service),
    token=Depends(get_current_user),
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        res = await receiver.update(id, update_schema.dict(exclude_unset=True))
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return res


@router.delete("/{id}")
async def delete(
    id: int,
    receiver: ReceiverServiceInterface = Depends(receiver_service),
    token=Depends(get_current_user),
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    await receiver.delete(id)
