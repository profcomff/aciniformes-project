from .crud import CrudService, FakeCrudService
from .scheduler import ApSchedulerService, FakeSchedulerService


class Config:
    fake: bool = True


def crud_service():
    if Config.fake:
        return FakeCrudService()
    return CrudService()


def scheduler_service():
    if Config.fake:
        return FakeSchedulerService(crud_service())
    return ApSchedulerService(crud_service())
