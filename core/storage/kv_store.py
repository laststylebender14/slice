import time
from abc import ABC, abstractmethod

from core.storage.options import Options
from core.storage.node import Node
from core.utils.time_utils import convert_to_absolute_expiray_in_ms, convert_time_to_ms

class Store(ABC):
    @abstractmethod
    def set_nx(self, key: str, value :Node, options: Options) -> int:
        pass
    @abstractmethod
    def set_xx(self, key: str, value :Node, options: Options) -> int:
        pass
    @abstractmethod
    def set(self, key: str, value :Node, options: Options) -> int:
        pass
    @abstractmethod
    def get(self, key: str, value: Node) -> Node:
        pass
    @abstractmethod
    def delete(self, key:str) -> bool:
        pass
    @abstractmethod
    def exists(self,key:str) -> bool:
        pass
    @abstractmethod
    def store(self):
        pass

KEY_VALUE_NOT_EXISTS = -1
KEY_VALUE_NOT_INSERTED = 0
KEY_VALUE_INSERTED = 1

class KVStore(Store):
    _instance = None
    def __new__(cls, *args,**kwargs) -> Store:
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
        
    def normalize_ttl(self, value:Node|None ,options: Options) -> Node:
        """ 
            depending on the options set, this function returns absolute expiry time.
        """
        if value.ttl:
            if options == Options.EX:
                value.ttl = convert_time_to_ms() + int(value.ttl,10) #TODO: handle the possibility of user passing non int values.
            else:
                value.ttl = convert_to_absolute_expiray_in_ms(int(value.ttl,10))
        return value
        
        
    def set_nx(self,key: str, value: Node | None, options:Options = None) -> int:
        """ set if key doesn't exists"""
        if self.exists(key):
            return KEY_VALUE_NOT_EXISTS
        
        normalizedValue = self.normalize_ttl(value, options)        
        print("[Store]:","[setnx]:",f"{key} inserted into db")
        self.store[key] = normalizedValue
        return KEY_VALUE_INSERTED
    
    def set_xx(self, key: str, value: Node | None, options:Options = None) -> int:
        if not self.exists(key):
            return KEY_VALUE_NOT_EXISTS
        normalizedValue = self.normalize_ttl(value, options)        
        print("[Store]:","[set_xx]:",f"{key} inserted into db")
        self.store[key] = normalizedValue
        return KEY_VALUE_INSERTED
        
    def set(self, key: str, value: Node, options:Options = None) -> int | None:        
        if options == Options.NX:
            return self.set_nx(key,value,options)
        if options == Options.XX:
            return self.set_xx(key,value,options)
        else:
            print("[Store]:","[set]:",f"{key} inserted into db")
            self.store[key] = self.normalize_ttl(value, options)
            return KEY_VALUE_INSERTED

    def get(self, key) -> Node | int:
        if self.exists(key):
            return self.store[key]
        return KEY_VALUE_NOT_EXISTS
        
            
    def delete(self, key) -> bool:
        if key in self.store:
            del self.store[key]
            print("[Store]:",f"{key} deleted from db")
            return True
        return False
    
    def store(self) -> dict[str, Node]:
        return self.store
    
    def __str__(self) -> str:
        return str(self.store)