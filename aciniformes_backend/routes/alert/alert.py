from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel, Json
from aciniformes_backend.models.alerts import Alert


class CreateSchema(BaseModel):
    data: Json
    reciever_id: int
    filter: str


class UpdateSchema(BaseModel):
    data: Json
    reciever_id: int
    filter: str


class GetReciever(BaseModel):
    pass


class GetSchema(BaseModel):
    id_: int
    data: Json
    reciever_id: GetReciever
    filter_: str
    create_ts: datetime
    modify_ts: datetime


router = APIRouter()


@router.post('')
def create():
    pass


@router.get('')
def get_all():
    pass


@router.get("/{id}")
def get(id: int):
    pass


@router.patch("/{id}")
def update(id: int):
    pass


@router.delete("/{id}")
def delete(id: int):
    pass
