from abc import ABC, abstractmethod
from core.storage.node import Node
from core.storage.options import Options
from core.constants.operation_return_constants import StorageOperationReturnType


class IStore(ABC):
    @abstractmethod
    def set_nx(self, key: str, value: Node, options: Options) -> StorageOperationReturnType:
        pass

    @abstractmethod
    def set_xx(self, key: str, value: Node, options: Options) -> StorageOperationReturnType:
        pass

    @abstractmethod
    def set(self, key: str, value: Node, options: Options) -> StorageOperationReturnType:
        pass

    @abstractmethod
    def get(self, key: str, value: Node) -> Node | StorageOperationReturnType:
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    def store(self) -> dict[str, Node]:
        pass

    @abstractmethod
    def ttl(self, key: str) -> int | StorageOperationReturnType | None:
        pass
