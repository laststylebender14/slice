from time import time
from config import WalConfig

def convert_second_to_ms(time_in_second: int) -> int:
    return int(time_in_second * 1000)

def convert_second_to_absolute_expiray_in_ms(time_in_second: int) -> int:
    return convert_second_to_ms(time()) + convert_second_to_ms(time_in_second)
def convert_time_to_ms() -> int:
    return convert_second_to_ms(time())


def convert_ms_to_seconds(time_in_ms: int) -> int:
    return int(time_in_ms / 1000)


def normalize_ttl(ttl_in_ms: int) -> int:
    return ttl_in_ms - WalConfig()._ttl_normalizer


def de_normalize_ttl(normalized_ttl: int) -> int:
    return normalized_ttl + WalConfig()._ttl_normalizer
