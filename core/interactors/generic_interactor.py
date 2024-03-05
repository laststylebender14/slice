from time import time
from core.storage import IStore
from core.constants.operation_return_constants import StorageOperationReturnType
from exceptions import (
    KeyNotExists,
    TTLNotExists,
)
from core.utils.time_utils import convert_ms_to_seconds

class GenericInteractor:
    def __init__(self, store: IStore) -> None:
        self.store = store
    
    def ttl(self, key: str) -> int | StorageOperationReturnType:
        ttl = self.store.ttl(key)
        if isinstance(ttl, StorageOperationReturnType):
            raise KeyNotExists(f"ERR didn't find the key you're looking for.")
        if ttl is None:
            raise TTLNotExists(f"ERR ttl doesn't exists with associated key.")
        return convert_ms_to_seconds(ttl) - int(time())