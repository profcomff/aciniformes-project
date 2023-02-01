class SessionNotInitializedError(Exception):
    def __init__(self):
        super().__init__(f"DB Session not initialized")


class ObjectNotFound(Exception):
    def __init__(self, key):
        super().__init__(f"Object not found: {key}")


class AlreadyRegistered(Exception):
    def __init__(self, username):
        super().__init__(f"User with {username} already registered")


class NotRegistered(Exception):
    def __init__(self, username):
        super().__init__(f"Username {username} not registered yet")


class WrongPassword(Exception):
    def __init__(self):
        super().__init__(f"Incorrect password")
