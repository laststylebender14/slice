from enum import Enum

class StorageOperationReturnType(Enum):
    KEY_VALUE_NOT_EXISTS = -1
    KEY_VALUE_NOT_INSERTED = 0
    KEY_VALUE_INSERTED = 1