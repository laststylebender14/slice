from core.storage.kv_store import Store
from core.storage.node import Node

from core.types import StructureType
from exceptions import (
    InvalidValueType,
    IncompatibleValueType,
    KeyNotExists,
    OperationFailed,
)
from core.storage.options import Options
from core.constants.operation_return_constants import StorageOperationReturnType


class StringInteractor:
    def __init__(self, store: Store) -> None:
        self.store = store

    def setnx(
        self, key: str, value: Node, options: Options = None
    ) -> StorageOperationReturnType:
        if not isinstance(value.value, str):
            raise InvalidValueType("ERR value must be a string.")
        value.type = StructureType.STRING
        resp: StorageOperationReturnType = self.store.set_nx(key, value, options)
        if resp != StorageOperationReturnType.KEY_VALUE_INSERTED:
            raise OperationFailed("ERR key already exists")
        return resp

    def setxx(
        self, key: str, value: Node, options: Options = None
    ) -> StorageOperationReturnType:
        if not isinstance(value.value, str):
            raise InvalidValueType("ERR value must be a string.")
        value.type = StructureType.STRING
        resp: StorageOperationReturnType = self.store.set_xx(key, value, options)
        if resp != StorageOperationReturnType.KEY_VALUE_INSERTED:
            raise OperationFailed("ERR key already not exists")
        return resp

    def set(
        self, key: str, value: Node, options: Options = None
    ) -> StorageOperationReturnType:
        if not isinstance(value.value, str):
            raise InvalidValueType("ERR value must be a string.")
        value.type = StructureType.STRING
        resp: StorageOperationReturnType = self.store.set(key, value, options)
        if resp != StorageOperationReturnType.KEY_VALUE_INSERTED:
            raise OperationFailed("ERR record not inserted.")
        return resp
        
    def get(self, key: str) -> Node:
        resp: Node | None | StorageOperationReturnType = self.store.get(key)
        if isinstance(resp, Node) and resp.type != StructureType.STRING:
            raise IncompatibleValueType(
                f"ERR required {StructureType.STRING.name} but found {resp.type.name}"
            )
        if resp is None:
            raise IncompatibleValueType(
                f"ERR required {StructureType.STRING.name} but found {None}"
            )
        if resp == StorageOperationReturnType.KEY_VALUE_NOT_EXISTS:
            raise KeyNotExists(f"ERR didn't find the key you're looking for")
        return resp

    def delete(self, key: str) -> Node:
        resp: Node = self.store.get(key)
        if self.store.delete(key):
            return resp
        raise OperationFailed(f"Failed to delete the key")
