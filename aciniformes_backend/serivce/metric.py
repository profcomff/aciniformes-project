import sqlalchemy as sa

from .base import MetricServiceInterface
import aciniformes_backend.models as db_models
import aciniformes_backend.serivce.exceptions as exc


class PgMetricService(MetricServiceInterface):
    async def create(self, item: dict) -> int:
        q = sa.insert(db_models.Metric).values(**item).returning(db_models.Metric)
        metric = self.session.scalar(q)
        self.session.flush()
        return metric.id_

    async def get_by_id(self, id_: int) -> db_models.Metric:
        q = sa.select(db_models.Metric).where(db_models.Metric.id_ == id_)
        res = self.session.scalar(q)
        if not res:
            raise exc.ObjectNotFound(id_)
        return res

    async def get_all(self) -> list[db_models.BaseModel]:
        return list(self.session.scalars(sa.select(db_models.Metric)).all())
