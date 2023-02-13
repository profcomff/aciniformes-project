from starlette import status


class TestAsgi:
    def test_schedule_success(self, ping_client, crud_client):
        res = ping_client.post('/schedule')
        assert res.status_code == status.HTTP_200_OK
        assert res.json() is None

    def test_start(self, ping_client):
        res = ping_client.get('/start')
        assert res.status_code == status.HTTP_200_OK
        ping_client.get('/stop')

    def test_start_already_started(self, ping_client):
        ping_client.get('/start')
        res2 = ping_client.get('/start')
        assert res2.status_code == status.HTTP_409_CONFLICT

    def test_stop(self, ping_client):
        pass

    def test_get_active_jobs(self, ping_client):
        pass

    def test_delete_schedulers(self, ping_client):
        pass
