class SessionNotInitializedError(Exception):
    def __init__(self):
        super().__init__(f"DB Session not initialized")


class InvalidUrl(Exception):
    def __init__(self, url):
        super().__init__(f"Invalid Url: {url}")


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


class WrongToken(Exception):
    def __init__(self):
        super().__init__(f"Could not decode token")
