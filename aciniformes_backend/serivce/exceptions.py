class ObjectNotFound(Exception):
    def __init__(self, key):
        super().__init__(f"Object not found: {key}")


