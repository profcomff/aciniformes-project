from sqlalchemy import *
from sqlalchemy import __all__ as sqlalchemy_all
from sqlalchemy.orm import as_declarative


__all__ = sqlalchemy_all + ("BaseModel",)


@as_declarative()
class BaseModel:
    def __tablename__(cls):
        return cls.__name__.lower()
