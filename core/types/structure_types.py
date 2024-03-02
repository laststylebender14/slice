from enum import Enum

"""
Maintains the data structure types currently supported by Slice DB.
"""
class StructureType(Enum):
    STRING = 1
    BLOOM_FILTER = 2 # Represents a type of space-efficient set data structure.
