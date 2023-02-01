from abc import ABC, abstractmethod


class CrudServiceInterface(ABC):
    @abstractmethod
    async def get_fetcher(self):
        raise NotImplementedError

    @abstractmethod
    async def get_metric(self):
        raise NotImplementedError

    @abstractmethod
    async def add_metric(self):
        raise NotImplementedError

    @abstractmethod
    async def add_alert(self):
        raise NotImplementedError


class CrudService(CrudServiceInterface):
    pass


class FakeCrudService(CrudServiceInterface):
    pass
