from abc import ABC, abstractmethod

from core.storage.options import Options
from core.storage.node import Node
from core.utils.time_utils import (
    convert_second_to_absolute_expiray_in_ms,
    convert_time_to_ms,
)
from core.constants.operation_return_constants import StorageOperationReturnType
from core.logger.logger import get_logger


class Store(ABC):
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


class KVStore(Store):
    _instance = None

    def __new__(cls, *args, **kwargs) -> Store:
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.store: dict[str, Node] = {}

    def exists(self, key: str) -> bool:
        if key not in self.store:
            return False
        if self.store[key].is_node_expired():
            # if expired then delete it.
            if self.delete(key):
                return False
        return True

    def normalize_ttl(self, value: Node | None, options: Options) -> Node:
        """
        depending on the options set, this function returns absolute expiry time.
        """
        if value.ttl is not None and value.ttl > 0:
            if options == Options.EX:
                value.ttl = convert_time_to_ms() + value.ttl
            else:
                value.ttl = convert_second_to_absolute_expiray_in_ms(value.ttl)
        return value

    def set_nx(
        self, key: str, value: Node | None, options: Options = None
    ) -> StorageOperationReturnType:
        """set if key doesn't exists"""
        if self.exists(key):
            return StorageOperationReturnType.KEY_VALUE_NOT_INSERTED

        normalizedValue = self.normalize_ttl(value, options)
        get_logger().info(f"[set_nx]: {key} inserted into db")
        self.store[key] = normalizedValue
        return StorageOperationReturnType.KEY_VALUE_INSERTED

    def set_xx(
        self, key: str, value: Node | None, options: Options = None
    ) -> StorageOperationReturnType:
        if not self.exists(key):
            return StorageOperationReturnType.KEY_VALUE_NOT_INSERTED
        normalizedValue = self.normalize_ttl(value, options)
        get_logger().info(f"[set_xx]: {key} inserted into db")
        self.store[key] = normalizedValue
        return StorageOperationReturnType.KEY_VALUE_INSERTED

    def set(
        self, key: str, value: Node, options: Options = None
    ) -> StorageOperationReturnType:
        if options == Options.NX:
            return self.set_nx(key, value, options)
        if options == Options.XX:
            return self.set_xx(key, value, options)
        else:
            get_logger().info(f"[set]: {key} inserted into db")
            self.store[key] = self.normalize_ttl(value, options)
            return StorageOperationReturnType.KEY_VALUE_INSERTED

    def get(self, key) -> Node | StorageOperationReturnType:
        if self.exists(key):
            return self.store[key]
        return StorageOperationReturnType.KEY_VALUE_NOT_EXISTS

    def delete(self, key) -> bool:
        if key in self.store:
            del self.store[key]
            get_logger().info(f"[delete]: {key} deleted from db")
            return True
        return False

    def store(self) -> dict[str, Node]:
        return self.store

    def __str__(self) -> str:
        return str(self.store)
