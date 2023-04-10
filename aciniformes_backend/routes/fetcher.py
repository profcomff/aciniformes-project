import logging

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, HttpUrl
from starlette import status

from aciniformes_backend.serivce import FetcherServiceInterface
from aciniformes_backend.serivce import exceptions as exc
from aciniformes_backend.serivce import fetcher_service

logger = logging.getLogger(__name__)
router = APIRouter()


class CreateSchema(BaseModel):
    name: str
    type_: str
    address: str
    fetch_data: str
    metrics: dict
    metric_name: str
    delay_ok: int
    delay_fail: int


class ResponsePostSchema(CreateSchema):
    id: int | None


class UpdateSchema(BaseModel):
    name: str | None
    type_: str | None
    address: HttpUrl | None
    fetch_data: str | None
    metrics: dict | None
    metric_name: str | None
    delay_ok: int | None
    delay_fail: int | None


class GetSchema(BaseModel):
    id: int


@router.post("", response_model=ResponsePostSchema)
async def create(
    create_schema: CreateSchema,
    fetcher: FetcherServiceInterface = Depends(fetcher_service),
    user=Depends(UnionAuth(["pinger.fetcher.create"])),
):
    id_ = await fetcher.create(create_schema.dict())
    return ResponsePostSchema(**create_schema.dict(), id=id_)


@router.get("")
async def get_all(
    fetcher: FetcherServiceInterface = Depends(fetcher_service),
):
    res = await fetcher.get_all()
    return res


@router.get("/{id}")
async def get(
    id: int,
    fetcher: FetcherServiceInterface = Depends(fetcher_service),
):
    try:
        res = await fetcher.get_by_id(id)
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return res


@router.patch("/{id}")
async def update(
    id: int,
    update_schema: UpdateSchema,
    fetcher: FetcherServiceInterface = Depends(fetcher_service),
    user=Depends(UnionAuth(["pinger.fetcher.update"])),
):
    try:
        res = await fetcher.update(id, update_schema.dict(exclude_unset=True))
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return res


@router.delete("/{id}")
async def delete(
    id: int,
    fetcher: FetcherServiceInterface = Depends(fetcher_service),
    user=Depends(UnionAuth(["pinger.fetcher.delete"])),
):
    await fetcher.delete(id)
