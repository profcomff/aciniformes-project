import pytest
from ping.service import Config


@pytest.fixture
def pg_config():
    Config.fake = False
    yield Config()


class TestSchedulerService:
    @pytest.mark.asyncio
    async def test_add_fetcher_success(self):
        pass

    @pytest.mark.asyncio
    async def test_delete_fetcher(self):
        pass

    @pytest.mark.asyncio
    async def test_get_jobs(self):
        pass

    @pytest.mark.asyncio
    async def test_start_success(self):
        pass

    @pytest.mark.asyncio
    async def test_start_alrady_started(self):
        pass

    @pytest.mark.asyncio
    async def test_stop(self):
        pass

    @pytest.mark.asyncio
    async def test_stop_already_stopped(self):
        pass

    @pytest.mark.asyncio
    async def test_write_alert(self):
        pass
