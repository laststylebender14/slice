from core.storage import Options

class AOFEntry:
    def __init__(self, key: str, value=None, ttl=None, options: Options = None ):
        self.key = key
        self.value = value
        self.ttl = ttl
        self.options = options
    def __str__(self):
        return f"Key: {self.key}, Value: {self.value}, TTL: {self.ttl}, Options: {self.options}"
