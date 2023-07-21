import os
import sys

import sqlalchemy as sa


sys.path.append(os.path.realpath('..'))

import models as db_models

from .base import FetcherServiceInterface
from .exceptions import ObjectNotFound


class PgFetcherService(FetcherServiceInterface):
    async def create(self, item: dict) -> int:
        q = sa.insert(db_models.Fetcher).values(**item).returning(db_models.Fetcher)
        fetcher = self.session.scalar(q)
        self.session.flush()
        return fetcher.id_

    async def get_by_id(self, id_: int) -> db_models.Fetcher:
        q = sa.select(db_models.Fetcher).where(db_models.Fetcher.id_ == id_)
        res = self.session.scalar(q)
        if not res:
            raise ObjectNotFound(id_)
        return res

    async def delete(self, id_: int) -> None:
        q = sa.delete(db_models.Fetcher).where(db_models.Fetcher.id_ == id_)
        self.session.execute(q)
        self.session.flush()

    async def update(self, id_: int, item: dict) -> db_models.Fetcher:
        q = sa.update(db_models.Fetcher).where(db_models.Fetcher.id_ == id_).values(**item).returning(db_models.Fetcher)
        if not await self.get_by_id(id_):
            raise ObjectNotFound(id_)
        res = self.session.execute(q).scalar()
        return res

    async def get_all(self) -> list[db_models.BaseModel]:
        return list(self.session.scalars(sa.select(db_models.Fetcher)).all())
