import os
import sys
from typing import Type

import sqlalchemy as sa


sys.path.append(os.path.realpath('..'))

import models as db_models

from .base import ReceiverServiceInterface
from .exceptions import ObjectNotFound


class PgReceiverService(ReceiverServiceInterface):
    async def create(self, item: dict) -> int:
        q = sa.insert(db_models.Receiver).values(**item).returning(db_models.Receiver)
        receiver = self.session.execute(q).scalar()
        self.session.flush()
        return receiver.id_

    async def get_by_id(self, id_: int) -> Type[db_models.Receiver]:
        q = sa.select(db_models.Receiver).where(db_models.Receiver.id_ == id_)
        res = self.session.scalar(q)
        if not res:
            raise ObjectNotFound(id_)
        return res

    async def delete(self, id_: int) -> None:
        q = sa.delete(db_models.Receiver).where(db_models.Receiver.id_ == id_)
        self.session.execute(q)
        self.session.flush()

    async def update(self, id_: int, item: dict) -> Type[db_models.Receiver]:
        q = (
            sa.update(db_models.Receiver)
            .where(db_models.Receiver.id_ == id_)
            .values(**item)
            .returning(db_models.Receiver)
        )
        if not self.get_by_id(id_):
            raise ObjectNotFound(id_)
        res = self.session.execute(q).scalar()
        return res

    async def get_all(self) -> list[db_models.BaseModel]:
        return list(self.session.scalars(sa.select(db_models.Receiver)).all())
