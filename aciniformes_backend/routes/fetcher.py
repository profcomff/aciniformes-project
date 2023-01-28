from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette import status
from pydantic import BaseModel, Json
from aciniformes_backend.serivce import (
    FetcherServiceInterface,
    fetcher_service,
    exceptions as exc,
)


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
    id: int


class UpdateSchema(BaseModel):
    name: str | None
    type_: str | None
    address: str | None
    fetch_data: str | None
    metrics: dict | None
    metric_name: str | None
    delay_ok: int | None
    delay_fail: int | None


class GetSchema(BaseModel):
    id: int


router = APIRouter()


@router.post("", response_model=ResponsePostSchema)
async def create(
    create_schema: CreateSchema,
    fetcher: FetcherServiceInterface = Depends(fetcher_service),
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
):
    await fetcher.delete(id)
