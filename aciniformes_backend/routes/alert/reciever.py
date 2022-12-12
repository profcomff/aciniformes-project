from fastapi import APIRouter
from pydantic import BaseModel


class CreateSchema(BaseModel):
    pass


class UpdateSchema(BaseModel):
    pass


class GetSchema(BaseModel):
    id: int


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
