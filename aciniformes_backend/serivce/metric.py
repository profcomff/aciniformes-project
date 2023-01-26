from .base import MetricServiceInterface
import aciniformes_backend.models as db_models
import aciniformes_backend.serivce.exceptions as exc


class PgMetricService(MetricServiceInterface):
    async def get_by_id(self, id_: int) -> db_models.Metric:
        res = (
            self.session.query(db_models.Metric)
            .filter(db_models.Metric.id_ == id_)
            .one_or_none()
        )
        if not res:
            raise exc.ObjectNotFound(id_)
        return res

    async def get_all(self) -> list[db_models.BaseModel]:
        res = self.session.query(db_models.Metric).all()
        if not res:
            raise exc.ObjectNotFound("table empty")
        return res

    async def create(self, metrics) -> None:
        self.session.add(db_models.Metric(metrics=metrics))
