from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from starlette import status

from aciniformes_backend.serivce import ReceiverServiceInterface
from aciniformes_backend.serivce import exceptions as exc
from aciniformes_backend.serivce import receiver_service


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
    receiver: ReceiverServiceInterface = Depends(receiver_service)
):
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
    user=Depends(UnionAuth(["pinger.receiver.update"])),
):
    try:
        res = await receiver.update(id, update_schema.dict(exclude_unset=True))
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return res


@router.delete("/{id}")
async def delete(
    id: int,
    receiver: ReceiverServiceInterface = Depends(receiver_service),
    user=Depends(UnionAuth(["pinger.receiver.delete"])),
):
    await receiver.delete(id)
