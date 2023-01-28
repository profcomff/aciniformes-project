from sqlalchemy import *
from sqlalchemy import __all__ as sqlalchemy_all
from sqlalchemy.orm import as_declarative, declared_attr


__all__ = sqlalchemy_all + ["BaseModel"]


@as_declarative()
class BaseModel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
