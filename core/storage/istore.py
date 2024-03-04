from abc import ABC, abstractmethod
from core.storage.node import Node
from core.storage.options import Options

class IStore(ABC):
    @abstractmethod
    def set_nx(self, key: str, value: Node, options: Options) -> int:
        pass

    @abstractmethod
    def set_xx(self, key: str, value: Node, options: Options) -> int:
        pass

    @abstractmethod
    def set(self, key: str, value: Node, options: Options) -> int:
        pass

    @abstractmethod
    def get(self, key: str, value: Node) -> Node:
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    def store(self):
        pass
