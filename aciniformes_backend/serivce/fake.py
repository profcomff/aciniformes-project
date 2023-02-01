import pydantic

from .base import (
    AlertServiceInterface,
    ReceiverServiceInterface,
    FetcherServiceInterface,
    MetricServiceInterface,
    AuthServiceInterface,
)
import aciniformes_backend.serivce.exceptions as exc
import aciniformes_backend.models as db_models
from aciniformes_backend.settings import get_settings


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
        raise exc.ObjectNotFound(id_)

    async def delete(self, id_: int) -> None:
        self.repository[id_] = None

    async def update(self, id_: int, item: dict) -> db_models.Alert:
        if id_ in self.repository:
            self.repository[id_] = db_models.Alert(**item)
            return self.repository[id_]
        raise exc.ObjectNotFound(id_)

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
        raise exc.ObjectNotFound(id_)

    async def delete(self, id_: int) -> None:
        self.repository[id_] = None

    async def update(self, id_: int, item: dict) -> db_models.Receiver:
        if id_ in self.repository:
            self.repository[id_] = db_models.Receiver(**item)
            return self.repository[id_]
        raise exc.ObjectNotFound(id_)

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
        raise exc.ObjectNotFound(id_)

    async def delete(self, id_: int) -> None:
        self.repository[id_] = None

    async def update(self, id_: int, item: dict) -> db_models.Fetcher:
        if id_ in self.repository:
            self.repository[id_] = db_models.Fetcher(**item)
            return self.repository[id_]
        raise exc.ObjectNotFound(id_)

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
        if id_ in self.repository:
            return self.repository[id_]
        raise exc.ObjectNotFound(id_)

    async def get_all(self) -> list[db_models.BaseModel]:
        return list(self.repository.values())


class FakeAuthService(AuthServiceInterface):
    repository = []

    async def registrate_user(self, username, password) -> db_models.Auth | None:
        db_user = db_models.Auth(username=username, password=password)
        self.repository.append(db_user)
        return db_user

    async def authenticate_user(self, username, password) -> db_models.Auth | None:
        for auth in self.repository:
            if auth.password == password and auth.username == username:
                return auth
        raise exc.NotRegistered(username)

    async def get_user(self, username)-> db_models.Auth | None:
        for auth in self.repository:
            if auth.username == username:
                return auth
        raise exc.NotRegistered(username)

    @staticmethod
    async def _validate_password(db_password, inp_password):
        return get_settings().PWD_CONTEXT.verify(inp_password, db_password)
