from core.storage.node import Node
from core.storage.options import Options
from time import time

def convert_second_to_ms(time_in_second: int) -> int:
    return time_in_second * 1000

def convert_to_absolute_expiray_in_ms(time_in_second: int) -> int:
    return convert_second_to_ms(time()) + convert_second_to_ms(time_in_second)
        
def convert_time_to_ms() -> int:
    return convert_second_to_ms(time())