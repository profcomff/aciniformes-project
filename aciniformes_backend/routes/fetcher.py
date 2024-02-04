import logging

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, HttpUrl
from pydantic.functional_serializers import PlainSerializer
from starlette import status
from typing_extensions import Annotated

from aciniformes_backend.models.fetcher import FetcherType
from aciniformes_backend.serivce import FetcherServiceInterface
from aciniformes_backend.serivce import exceptions as exc
from aciniformes_backend.serivce import fetcher_service


logger = logging.getLogger(__name__)
router = APIRouter()


class CreateSchema(BaseModel):
    type_: FetcherType
    address: str
    fetch_data: str
    delay_ok: int
    delay_fail: int


class ResponsePostSchema(CreateSchema):
    id: int | None = None


class UpdateSchema(BaseModel):
    type_: FetcherType | None = None
    address: Annotated[HttpUrl, PlainSerializer(lambda x: str(x), return_type=str)] | None = None
    fetch_data: str | None = None
    delay_ok: int | None = None
    delay_fail: int | None = None


class GetSchema(BaseModel):
    id: int


@router.post("", response_model=ResponsePostSchema)
async def create(
    create_schema: CreateSchema,
    fetcher: FetcherServiceInterface = Depends(fetcher_service),
    _: dict[str] = Depends(UnionAuth(['pinger.fetcher.create'])),
):
    """
    Создает новый сборщик.
    """
    id_ = await fetcher.create(create_schema.model_dump())
    return ResponsePostSchema(**create_schema.model_dump(), id=id_)


@router.get("")
async def get_all(
    fetcher: FetcherServiceInterface = Depends(fetcher_service),
    _: dict[str] = Depends(UnionAuth(['pinger.fetcher.read'])),
):
    """
    Возвращает все сборщики.
    """
    res = await fetcher.get_all()
    return res


@router.get("/{id}")
async def get(
    id: int,
    fetcher: FetcherServiceInterface = Depends(fetcher_service),
    _: dict[str] = Depends(UnionAuth(['pinger.fetcher.read'])),
):
    """Получение одного сборщика по id"""
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
    _: dict[str] = Depends(UnionAuth(['pinger.fetcher.update'])),
):
    """Обновление одного сборика по id"""
    try:
        res = await fetcher.update(id, update_schema.model_dump(exclude_unset=True))
    except exc.ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return res


@router.delete("/{id}")
async def delete(
    id: int,
    fetcher: FetcherServiceInterface = Depends(fetcher_service),
    _: dict[str] = Depends(UnionAuth(['pinger.fetcher.delete'])),
):
    """Удаление одного сборика по id"""
    await fetcher.delete(id)
