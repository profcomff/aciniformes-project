from .base import FetcherServiceInterface
import aciniformes_backend.serivce.exceptions as exc
import aciniformes_backend.models as db_models


class PgFetcherService(FetcherServiceInterface):
    async def create(self, fetcher: dict) -> None:
        self.session.add(db_models.Fetcher(**fetcher))

    async def get_by_id(self, id_: int) -> db_models.Fetcher:
        res = (
            self.session.query(db_models.Fetcher)
            .filter(db_models.Fetcher.id_ == id_)
            .one_or_none()
        )
        if not res:
            raise exc.ObjectNotFound(id_)
        return res

    async def delete(self, id_: int) -> None:
        item = self.get_by_id(id_)
        self.session.delete(item)

    async def update(self, id_: int, item: dict) -> db_models.Fetcher:
        q = self.session.query(db_models.Fetcher).filter(db_models.Fetcher.id_ == id_)
        if not q.one_or_none():
            raise exc.ObjectNotFound(id_)
        q.update(**item)
        return q.one_or_none()

    async def get_all(self) -> list[db_models.BaseModel]:
        return self.session.query(db_models.Fetcher).all()
