from typing import List

from core.storage.kv_store import Store
from core.commandhandler.string_command_handler import StringCommandHandler
from core.resp.encoder import encode_simple_strings_resp, encode_bulk_strings_reps,encode_null_string_resp
from core.commandhandler.supported_commands import SupportedCommands


class CommandHandler:
    def __init__(self, store: Store, walFile) -> None:
        self.string_command_handler = StringCommandHandler(store=store, walFile=walFile)
            
    def handle(self, commands: List[str]) -> str:
        if isinstance(commands, List) and len(commands) > 0:
            command = commands[0].strip().lower()
            if command == SupportedCommands.PING.value:
                return encode_simple_strings_resp("pong")
            elif command == SupportedCommands.ECHO.value:
                return encode_simple_strings_resp(" ".join(commands[1:]))        
            elif command == SupportedCommands.GET.value:
                return self.string_command_handler.get(commands=commands[1:])
            elif command == SupportedCommands.SET.value:
                return self.string_command_handler.set(commands=commands[1:])
            elif command == SupportedCommands.GETDEL.value:
                return self.string_command_handler.delete(commands=commands[1:])
            elif command == SupportedCommands.SETNX.value:
                return self.string_command_handler.setnx(commands=commands[1:])
            elif command == SupportedCommands.SETXX.value:
                return self.string_command_handler.setxx(commands=commands[1:])
        return encode_bulk_strings_reps("Error syntax error")