from typing import List
from enum import Enum

from core.storage.kv_store import Store
from core.interactors.string_interactor import StringInteractor
from core.resp.encoder import (
    encode_simple_strings_resp,
    encode_bulk_strings_reps,
    encode_null_string_resp,
)
from core.storage.node import Node
from core.types.structure_types import StructureType
from core.storage.options import Options
from core.aof.aof import WAL
from core.utils.time_utils import (
    convert_second_to_absolute_expiray_in_ms,
    convert_time_to_ms,
)
from core.constants.operation_return_constants import StorageOperationReturnType
from exceptions import (
    InvalidValueType,
    IncompatibleValueType,
    KeyNotExists,
    OperationFailed,
)


class StringOptions(Enum):
    NX = "nx"
    XX = "xx"
    EX = "ex"
    PX = "px"


class StringCommandHandler:
    def __init__(self, store: Store, walFile: WAL = None) -> None:
        self.interactor = StringInteractor(store=store)
        self.walFile = walFile

    def log(self, log_line) -> None:
        if self.walFile:
            self.walFile.log(log_line)

    def setnx(self, commands: List[str]) -> str:
        """
        handles commands like:
        [setnx key value]
        """
        log_line = ",".join(commands)
        commands = commands[1:]
        commandSize = len(commands)
        if commandSize != 2:
            return encode_bulk_strings_reps("ERR Syntax error")

        try:
            key, value = commands
            self.interactor.setnx(
                key=key,
                value=Node(value=value, type=StructureType.STRING),
                options=Options("nx"),
            )
            self.log(log_line)
            return encode_simple_strings_resp("(integer) 1")
        except OperationFailed as err:
            return encode_simple_strings_resp("(integer) 0")
        except InvalidValueType as err:
            return encode_bulk_strings_reps(str(err))
        except Exception as err:
            return encode_bulk_strings_reps(str(err))

    def setxx(self, commands: List[str]) -> str:
        """
        handles commands like:
        [setxx key value]
        """
        log_line = ",".join(commands)
        commands = commands[1:]
        commandSize = len(commands)
        if commandSize != 2:
            return encode_bulk_strings_reps("ERR Syntax error")

        try:
            key, value = commands

            self.interactor.setxx(
                key=key,
                value=Node(value=value, type=StructureType.STRING),
                options=Options("xx"),
            )
            self.log(log_line)
            return encode_simple_strings_resp("(integer) 1")
        except OperationFailed as err:
            return encode_simple_strings_resp("(integer) 0")
        except InvalidValueType as err:
            return encode_bulk_strings_reps(str(err))
        except Exception as err:
            return encode_bulk_strings_reps(str(err))

    def set(self, commands: List[str]) -> str:
        """
        commands are in the form of.
        len(commands) ==  2 then  ["KEY","VALUE"]
        len(commands) ==  3 then  ["KEY","VALUE","NX/XX"]
        len(commands) ==  4 then  ["KEY","VALUE","EX/PX","EXP_TIME"]
        len(commands) ==  5 then  ["KEY","VALUE","NX/PX","EX/PX","EXP_TIME"]    TODO: provide support for 5th command.
        """
        log_line = ",".join(commands)
        logging_command = commands
        commands = commands[1:]

        commandSize = len(commands)
        if commandSize not in [2, 3, 4, 5]:
            return encode_bulk_strings_reps("ERR Syntax error")

        if commandSize == 2:
            try:
                key, value = commands
                self.interactor.set(
                    key=key, value=Node(value=value, type=StructureType.STRING)
                )
                self.log(log_line)
                return encode_simple_strings_resp("OK")
            except OperationFailed as err:
                return encode_null_string_resp()
            except InvalidValueType as err:
                return encode_bulk_strings_reps(str(err))
            except Exception as err:
                return encode_bulk_strings_reps(str(err))

        elif commandSize == 3:
            key, value, option = commands
            processedOption = option.strip().lower()

            if processedOption == StringOptions.XX.value:
                return self.setxx(commands[:-1])
            elif processedOption == StringOptions.NX.value:
                return self.setnx(commands[:-1])
            return encode_bulk_strings_reps("ERR Syntax error")

        elif commandSize == 4:
            key, value, exp_command, exp_time = commands
            try:
                expiration = int(exp_time, base=10)
                if expiration < 0:
                    raise ValueError("expiration time can't be negative")
            except ValueError:
                return encode_bulk_strings_reps(
                    "ERR value is not an integer or out of range"
                )
            processed_command = exp_command.strip().lower()
            processed_expiry_time = 0
            if processed_command not in ["ex", "px"]:
                return encode_bulk_strings_reps("ERR Syntax error")
            if processed_command == StringOptions.PX.value:
                processed_expiry_time = convert_second_to_absolute_expiray_in_ms(
                    expiration
                )
                options = Options("px")
            elif processed_command == StringOptions.EX.value:
                processed_expiry_time = convert_time_to_ms() + expiration
                options = Options("ex")

            # process ttl in iterms of absolute expiry for logging else keys will be refilled whenever aof loaded.
            # can't store ttl directly into aof file.
            # so store ttl as expired_at into log file, and while reading do (time.time() * 1000) ms conversion - expired_at = to get the remaining ttl value.
            # [key, value, ex, 200]
            try:
                self.interactor.set(
                    key=key,
                    value=Node(value=value, type=StructureType.STRING, ttl=expiration),
                    options=options,
                )
                logging_command[4] = str(processed_expiry_time)
                log_line = ",".join(logging_command)
                self.log(log_line)
                return encode_simple_strings_resp("OK")
            except OperationFailed as err:
                return encode_null_string_resp()
            except InvalidValueType as err:
                return encode_bulk_strings_reps(str(err))
            except Exception as err:
                return encode_bulk_strings_reps(str(err))
        return encode_null_string_resp()

    def get(self, commands: List[str]) -> str:
        """
        handles commands like:
        [get key]
        """
        commands = commands[1:]
        commandSize = len(commands)

        if commandSize != 1:
            return encode_bulk_strings_reps("ERR Syntax error")

        key = commands[0]
        try:
            resp: Node = self.interactor.get(key=key)
            return encode_bulk_strings_reps(resp=resp.value)
        except KeyNotExists as err:
            return encode_bulk_strings_reps(str(err))
        except IncompatibleValueType as err:
            return encode_bulk_strings_reps(str(err))
        except Exception as err:
            return encode_bulk_strings_reps("ERR Server side")

    def delete(self, commands: List[str]) -> str:
        """
        handles commands like:
        [getdel key]
        """
        log_line = ",".join(commands)
        commands = commands[1:]

        commandSize = len(commands)

        if commandSize != 1:
            return encode_bulk_strings_reps("ERR Syntax error")

        try:
            key = commands[0]
            resp: Node | None = self.interactor.delete(key=key)
            if resp:
                self.log(log_line)
                return encode_bulk_strings_reps(resp=resp.value)
        except KeyNotExists as err:
            return encode_bulk_strings_reps(str(err))
        except IncompatibleValueType as err:
            return encode_bulk_strings_reps(str(err))
        except OperationFailed as err:
            return encode_bulk_strings_reps(str(err))
        except Exception as err:
            return encode_bulk_strings_reps("ERR Server side")
