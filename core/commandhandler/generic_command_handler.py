from typing import List
from core.storage import IStore
from core.resp import (
    encode_simple_strings_resp,
    encode_integer
)
from core.interactors import GenericInteractor
from exceptions import (
    KeyNotExists,
    TTLNotExists,
)

class GenericCommandHandler:
    def __init__(self, store: IStore) -> None:
        self.generic_interactor = GenericInteractor(store=store)
    
    def ttl(self, commands: List[str]) -> str:
        """ 
            handles commands like 
            [ttl key]
        """
        commands = commands[1:]
        command_size = len(commands)
        if command_size != 1:
            return encode_simple_strings_resp("ERR Syntax error")

        key = commands[0]
        try:
            ttl = self.generic_interactor.ttl(key)
            return encode_integer(ttl)
        except TTLNotExists:
            return encode_integer(-1)
        except KeyNotExists:
            return encode_integer(-2)
        except Exception:
            return encode_simple_strings_resp("ERR Server side")