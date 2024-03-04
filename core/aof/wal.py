from abc import ABC, abstractmethod

class WAL(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def log(self, wal_entry: str) -> None:
        pass

    @abstractmethod
    def replay(self, command_handler = None):
        pass
