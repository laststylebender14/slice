import time
from core.types import StructureType
from core.utils.time_utils import de_normalize_ttl

"""
Class representing a node in the slice database.

Attributes:
  - value: The data value stored in the node. Can be of any type.
  - type: TODO: type will always be less than 256, figure out a way to store that in 1 byte.
  - ttl: Time-to-live of the node in milliseconds. Nodes expire after this duration.
          If None, the node doesn't expire.
"""
class Node:
    def __init__(self, value: any, type: StructureType, ttl: int|None = None) -> None:
        self.value = value
        self.type = type
        self.ttl = ttl

    def is_node_expired(self) -> bool:
        """Checks if the node has expired based on its TTL."""
        current_time_ms = int(time.time() * 1000)
        return self.ttl is not None and current_time_ms > de_normalize_ttl(self.ttl)

    def __str__(self):
        """Returns a string representation of the node's attributes."""
        return f"Value: {self.value}, Type: {self.type}, TTL: {self.ttl}"
