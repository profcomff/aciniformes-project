from .crud import CrudService, FakeCrudService
from .scheduler import ApSchedulerService, FakeSchedulerService


class Config:
    fake: bool = False


def crud_service():
    if Config.fake:
        return FakeCrudService()
    return CrudService()


def scheduler_service():
    if Config.fake:
        return FakeCrudService()
    return ApSchedulerService()