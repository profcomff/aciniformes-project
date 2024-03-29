from abc import ABC, abstractmethod

import sqlalchemy.orm

import aciniformes_backend.models as db_models


class BaseService(ABC):
    def __init__(self, session: sqlalchemy.orm.Session | None):
        self.session = session

    @abstractmethod
    async def get_all(self) -> list[db_models.BaseModel]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, item: dict) -> int:
        raise NotImplementedError


class AlertServiceInterface(BaseService):
    @abstractmethod
    async def get_by_id(self, id_: int) -> db_models.Alert:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id_: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id_: int, item: dict) -> db_models.Alert:
        raise NotImplementedError


class ReceiverServiceInterface(BaseService):
    @abstractmethod
    async def get_by_id(self, id_: int) -> db_models.Receiver:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id_: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id_: int, item: dict) -> db_models.Receiver:
        raise NotImplementedError


class FetcherServiceInterface(BaseService):
    @abstractmethod
    async def get_by_id(self, id_: int) -> db_models.Fetcher:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id_: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id_: int, item: dict) -> db_models.Fetcher:
        raise NotImplementedError


class MetricServiceInterface(BaseService):
    @abstractmethod
    async def get_by_id(self, id_: int) -> db_models.Metric:
        raise NotImplementedError
