from typing import List

from core.storage import IStore
from core.commandhandler.string_command_handler import StringCommandHandler
from core.resp import encode_simple_strings_resp
from core.commandhandler.supported_commands import SupportedCommands


class CommandHandler:
    def __init__(self, store: IStore, walFile) -> None:
        self.string_command_handler = StringCommandHandler(store=store, walFile=walFile)
            
    def handle(self, commands: List[str]) -> str:
        if isinstance(commands, List) and len(commands) > 0:
            command = commands[0].strip().lower()
            if command == SupportedCommands.TTL.value:
                return encode_simple_strings_resp("not implemented yet.")
            if command == SupportedCommands.PING.value:
                return encode_simple_strings_resp("PONG")
            elif command == SupportedCommands.ECHO.value:
                return encode_simple_strings_resp(" ".join(commands[1:]))        
            elif command == SupportedCommands.GET.value:
                return self.string_command_handler.get(commands=commands)
            elif command == SupportedCommands.SET.value:
                return self.string_command_handler.set(commands=commands)
            elif command == SupportedCommands.GETDEL.value:
                return self.string_command_handler.delete(commands=commands)
            elif command == SupportedCommands.SETNX.value:
                return self.string_command_handler.setnx(commands=commands)
            elif command == SupportedCommands.SETXX.value:
                return self.string_command_handler.setxx(commands=commands)
        return encode_simple_strings_resp("Error syntax error")