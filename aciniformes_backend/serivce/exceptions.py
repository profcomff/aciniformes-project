class ObjectNotFound(Exception):
    def __init__(self, key):
        super().__init__(f"Object not found: {key}")


class SessionNotInitializedError(Exception):
    def __init__(self):
        super().__init__(f"DB Session not initialized")
