import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Literal

from ping3 import ping as sync_ping


thread_pool = ThreadPoolExecutor()


async def ping(host: str) -> float | Literal[True, None]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(thread_pool, partial(sync_ping, host))
