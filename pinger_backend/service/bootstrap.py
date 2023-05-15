from .crud import CrudService, FakeCrudService
from .scheduler import ApSchedulerService, FakeSchedulerService


class Config:
    fake: bool = False


def crud_service():
    return FakeCrudService() if Config.fake else CrudService()


def scheduler_service():
    return FakeSchedulerService(crud_service()) if Config.fake else ApSchedulerService(crud_service())
