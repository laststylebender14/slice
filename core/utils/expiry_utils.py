from core.storage.node import Node
from core.storage.options import Options
import time

def normalize_ttl(value:Node|None ,options: Options) -> Node:
    """ 
        depending on the options set, this function returns absolute expiry time.
    """
    if value.ttl:
        if options == Options.EX:
            value.ttl = int(time.time() * 1000) + int(value.ttl,10) #TODO: handle the possibility of user passing non int values.
        else:
            value.ttl = int(time.time() * 1000) + (int(value.ttl,10) * 1000)
    return value
        