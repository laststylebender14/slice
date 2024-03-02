from core.storage.kv_store import Store
from core.storage.node import Node

from core.types import StructureType
from exceptions import InvalidValueType, IncompatibleValueType
from core.storage.options import Options

class StringInteractor:
    def __init__(self, store: Store) -> None:
        self.store = store
    
    def setnx(self, key: str, value : Node, options: Options = None) -> int:
        if not isinstance(value.value, str):
            raise InvalidValueType("value must be a string.")
        value.type = StructureType.STRING
        return self.store.set_nx(key,value, options)
    
    def setxx(self, key: str, value : Node,  options: Options = None) -> int:
        if not isinstance(value.value, str):
            raise InvalidValueType("value must be a string.")
        value.type = StructureType.STRING
        return self.store.set_xx(key,value, options)
    
    def set(self, key: str, value : Node,  options: Options = None) -> int:
        if not isinstance(value.value, str):
            raise InvalidValueType("value must be a string.")
        value.type = StructureType.STRING
        return self.store.set(key,value, options)
    
    def get(self, key: str) -> (Node | None):
        resp: (Node | None) = self.store.get(key)
        if resp is not None and resp.type != StructureType.STRING:
            raise IncompatibleValueType(f"required {StructureType.STRING.name} but found {resp.type.name}")
        return resp
    
    def delete(self, key: str) -> (Node | None):
        resp: (Node | None) = self.store.get(key)
        if resp is not None and resp.type != StructureType.STRING:
            raise IncompatibleValueType(f"required {StructureType.STRING.name} but found {resp.type.name}")
        if self.store.delete(key):
            return resp
        return None