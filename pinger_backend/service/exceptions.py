class AlreadyRunning(Exception):
    def __init__(self):
        super().__init__("Scheduler is already running")


class ConnectionFail(Exception):
    def __init__(self):
        super().__init__("Failed to connect while fetching")


class AlreadyStopped(Exception):
    def __init__(self):
        super().__init__("Scheduler is already stopped")