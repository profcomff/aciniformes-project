import pydantic

from .base import (
    AlertServiceInterface,
    ReceiverServiceInterface,
    FetcherServiceInterface,
    MetricServiceInterface,
)
import aciniformes_backend.models as db_models


class FakeAlertService(AlertServiceInterface):
    id_incr = 0
    repository = dict()

    def __init__(self, session):
        super().__init__(session)

    async def create(self, item: dict) -> int:
        self.repository[self.id_incr] = db_models.Alert(**item)
        self.id_incr += 1
        return self.id_incr

    async def get_by_id(self, id_: int) -> db_models.Alert:
        return self.repository[id_]

    async def delete(self, id_: int) -> None:
        self.repository[id_] = None

    async def update(self, id_: int, item: dict) -> db_models.Alert:
        self.repository[id_] = db_models.Alert(**item)
        return self.repository[id_]

    async def get_all(self) -> list[db_models.BaseModel]:
        return list(self.repository.values())


class FakeReceiverService(ReceiverServiceInterface):
    id_incr = 0
    repository = dict()

    def __init__(self, session):
        super().__init__(session)

    async def create(self, item: dict) -> int:
        self.repository[self.id_incr] = db_models.Receiver(**item)
        self.id_incr += 1
        return self.id_incr

    async def get_by_id(self, id_: int) -> db_models.Receiver:
        return self.repository[id_]

    async def delete(self, id_: int) -> None:
        self.repository[self.id_incr] = None

    async def update(self, id_: int, item: dict) -> db_models.Receiver:
        self.repository[id_] = db_models.Receiver(**item)
        return self.repository[id_]

    async def get_all(self) -> list[db_models.BaseModel]:
        return list(self.repository.values())


class FakeFetcherService(FetcherServiceInterface):
    id_incr = 0
    repository = dict()

    def __init__(self, session):
        super().__init__(session)

    async def create(self, item: dict) -> int:
        self.repository[self.id_incr] = db_models.Fetcher(**item)
        self.id_incr += 1
        return self.id_incr

    async def get_by_id(self, id_: int) -> db_models.Fetcher:
        return self.repository[id_]

    async def delete(self, id_: int) -> None:
        self.repository[id_] = None

    async def update(self, id_: int, item: dict) -> db_models.Fetcher:
        self.repository[id_] = db_models.Fetcher(**item)
        return self.repository[id_]

    async def get_all(self) -> list[db_models.BaseModel]:
        return list(self.repository.values())


class FakeMetricService(MetricServiceInterface):
    id_incr = 0
    repository = dict()

    def __init__(self, session):
        super().__init__(session)

    async def create(self, item: dict) -> int:
        self.repository[self.id_incr] = db_models.Fetcher(**item)
        self.id_incr += 1
        return self.id_incr

    async def get_by_id(self, id_: int) -> db_models.Metric:
        return self.repository[id_]

    async def get_all(self) -> list[db_models.BaseModel]:
        return list(self.repository.values())
