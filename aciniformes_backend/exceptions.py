class AlreadyRunning(Exception):
    def __init__(self):
        super().__init__("Scheduler is already running")


class AlreadyStopped(Exception):
    def __init__(self):
        super().__init__("Scheduler is already stopped")
