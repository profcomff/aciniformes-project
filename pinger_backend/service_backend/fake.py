import os
import sys


sys.path.append(os.path.realpath('..'))

import models as db_models

from .base import AlertServiceInterface, FetcherServiceInterface, MetricServiceInterface, ReceiverServiceInterface
from .exceptions import ObjectNotFound


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
        if id_ in self.repository:
            return self.repository[id_]
        raise ObjectNotFound(id_)

    async def delete(self, id_: int) -> None:
        self.repository[id_] = None

    async def update(self, id_: int, item: dict) -> db_models.Alert:
        if id_ in self.repository:
            self.repository[id_] = db_models.Alert(**item)
            return self.repository[id_]
        raise ObjectNotFound(id_)

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
        if id_ in self.repository:
            return self.repository[id_]
        raise ObjectNotFound(id_)

    async def delete(self, id_: int) -> None:
        self.repository[id_] = None

    async def update(self, id_: int, item: dict) -> db_models.Receiver:
        if id_ in self.repository:
            self.repository[id_] = db_models.Receiver(**item)
            return self.repository[id_]
        raise ObjectNotFound(id_)

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
        if id_ in self.repository:
            return self.repository[id_]
        raise ObjectNotFound(id_)

    async def delete(self, id_: int) -> None:
        self.repository[id_] = None

    async def update(self, id_: int, item: dict) -> db_models.Fetcher:
        if id_ in self.repository:
            self.repository[id_] = db_models.Fetcher(**item)
            return self.repository[id_]
        raise ObjectNotFound(id_)

    async def get_all(self) -> list[db_models.BaseModel]:
        return list(self.repository.values())


class FakeMetricService(MetricServiceInterface):
    id_incr = 0
    repository = dict()

    def __init__(self, session):
        super().__init__(session)

    async def create(self, item: dict) -> int:
        self.repository[self.id_incr] = db_models.Metric(**item)
        self.id_incr += 1
        return self.id_incr

    async def get_by_id(self, id_: int) -> db_models.Metric:
        if id_ in self.repository:
            return self.repository[id_]
        raise ObjectNotFound(id_)

    async def get_all(self) -> list[db_models.BaseModel]:
        return list(self.repository.values())
