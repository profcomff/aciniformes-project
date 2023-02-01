from abc import ABC, abstractmethod
import asyncio
import aioschedule as schedule


class PingServiceInterface(ABC):
    event_loop: asyncio.BaseEventLoop

    @abstractmethod
    async def add_event(self, event):
        raise NotImplementedError


class PingService(PingServiceInterface):
    async def add_event(self, event):
        schedule.every(1).second.run(event)
        self.event_loop.run_until_complete(schedule.run_pending())