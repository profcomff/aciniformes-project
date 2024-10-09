import sqlalchemy as sa

import aciniformes_backend.models as db_models
import aciniformes_backend.service.exceptions as exc

from .base import AlertServiceInterface


class PgAlertService(AlertServiceInterface):
    async def create(self, item: dict) -> int:
        q = sa.insert(db_models.Alert).values(**item).returning(db_models.Alert)
        alert = self.session.execute(q).scalar()
        self.session.flush()
        return alert.id_

    async def get_by_id(self, id_: int) -> db_models.Alert:
        q = sa.select(db_models.Alert).where(db_models.Alert.id_ == id_)
        res = self.session.execute(q).scalar()
        if not res:
            raise exc.ObjectNotFound(id_)
        return res

    async def delete(self, id_: int) -> None:
        q = sa.delete(db_models.Alert).where(db_models.Alert.id_ == id_)
        self.session.execute(q)
        self.session.flush()

    async def update(self, id_: int, item: dict) -> db_models.Alert:
        q = sa.update(db_models.Alert).where(db_models.Alert.id_ == id_).values(**item).returning(db_models.Alert)
        if not await self.get_by_id(id_):
            raise exc.ObjectNotFound(id_)
        res = self.session.execute(q).scalar()
        return res

    async def get_all(self) -> list[db_models.BaseModel]:
        return list(self.session.scalars(sa.select(db_models.Alert)).all())
