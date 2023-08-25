import logging
from enum import Enum

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from starlette import status
from auth_lib.fastapi import UnionAuth

from aciniformes_backend.serivce import ReceiverServiceInterface
from aciniformes_backend.serivce import exceptions as exc
from aciniformes_backend.serivce import receiver_service


logger = logging.getLogger(__name__)


class Method(str, Enum):
    POST: str = "post"
    GET: str = "get"


class CreateSchema(BaseModel):
    url: str
    method: Method
    receiver_body: dict[str, str | int | list]


class PostResponseSchema(CreateSchema):
    url: str | None = None
    method: Method
    receiver_body: dict[str, str | int | list] | None = None


class UpdateSchema(BaseModel):
    url: str | None
    method: Method | None
    receiver_body: dict[str, str | int | list] | None = None


class GetSchema(BaseModel):
    url: str
    method: Method
    receiver_body: dict[str, str | int | list] | None = None


router = APIRouter()


@router.post("", response_model=PostResponseSchema)
async def create(
    create_schema: CreateSchema,
    receiver: ReceiverServiceInterface = Depends(receiver_service),
    _: dict[str, str] = Depends(UnionAuth(['pinger.reciever.create'])),
):
    id_ = await receiver.create(create_schema.model_dump())
    return PostResponseSchema(**create_schema.model_dump(), id=id_)


@router.get("")
async def get_all(
    receiver: ReceiverServiceInterface = Depends(receiver_service),
    _: dict[str, str] = Depends(UnionAuth(['pinger.reciever.read'])),
):
    res = await receiver.get_all()
    return res


@router.get("/{id}")
async def get(
    id: int,
    receiver: ReceiverServiceInterface = Depends(receiver_service),
    _: dict[str, str] = Depends(UnionAuth(['pinger.reciever.read'])),
):
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
    _: dict[str, str] = Depends(UnionAuth(['pinger.reciever.update'])),
):
    try:
        res = await receiver.update(id, update_schema.model_dump(exclude_unset=True))
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return res


@router.delete("/{id}")
async def delete(
    id: int,
    receiver: ReceiverServiceInterface = Depends(receiver_service),
    _: dict[str, str] = Depends(UnionAuth(['pinger.reciever.delete'])),
):
    await receiver.delete(id)
