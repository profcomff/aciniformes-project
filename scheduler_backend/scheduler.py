# from ping.service.scheduler import ApSchedulerService
# from ping.service.crud import CrudServiceInterface
#
# import httpx
# from aciniformes_backend.settings import get_settings
#
#
# class Scheduler(ApSchedulerService):
#     scheduler = ApSchedulerService.scheduler
#     settings = get_settings()
#     crud_service = CrudServiceInterface
#     paused = False
#
#     def __init__(self):
#         self.start()
#
#     @class
#     def start(self):
#         fetchers = httpx.get(f"{self.settings.DB_DSN}/fetcher").json()
#         for fetcher in fetchers:
#             self._fetch_it(fetcher)
