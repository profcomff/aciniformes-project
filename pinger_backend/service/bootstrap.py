from .crud import CrudService
from .scheduler import ApSchedulerService


class Config:
    fake: bool = False


def crud_service():
    return CrudService()


def scheduler_service():
    return ApSchedulerService(crud_service())
