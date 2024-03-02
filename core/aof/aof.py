from zlib import crc32
from abc import abstractmethod

from .aof_entry import AOFEntry
from core.commandhandler.supported_commands import SupportedCommands
from core.storage.options import Options

def calculate_crc(data_string: str) -> int:
    """Calculates the CRC32 checksum for the provided data string."""
    return crc32(data_string.encode())

class WAL:
    def __init__(self) -> None:
        pass
    @abstractmethod
    def log(self,operation: SupportedCommands,entry: AOFEntry) ->None:
        pass

""" 
    log file format: CRC,timestamp,operation,key,value,ttl
"""
class AOF:
    def __init__(self, log_file_path: str, separator: str = ","):
        self.log_file = open(log_file_path, "a")  # Open file for append
        self.separator = separator
        
    def flush_to_disk(self):
        self.log_file.flush()

    def log(self, operation: SupportedCommands, entry: AOFEntry) -> None:
        """
        Appends an operation and its associated data to the AOF file.

        Args:
            operation: The AOF operation (e.g., SET, DELETE).
            entry: AOFEntry that needs to be logged in file.
        """
        if self.log_file:
            data_string = f"{operation.value},{entry.key}"
            if entry.value is not None:
                data_string += f"{self.separator}{entry.value}"
            if entry.ttl is not None:
                data_string += f"{self.separator}{entry.ttl}"
            if entry.options is not None:
                if entry.options == Options.EX:
                    data_string += f"{self.separator}ex"
                elif entry.options == Options.PX:
                    data_string += f"{self.separator}px"
                elif entry.options == Options.NX:
                    data_string += f"{self.separator}nx"
                elif entry.options == Options.XX:
                    data_string += f"{self.separator}xx"
            log_line = f"{calculate_crc(data_string)},{data_string}\n"
            print("[LogLine]:", log_line)
            self.log_file.write(log_line)
            return True
        return False

    def close(self):
        """Closes the AOF file."""
        self.flush_to_disk()
        self.log_file.close()

    def replay(self, command_handler) -> None:
        """
        Replays the logged operations from the AOF file into the provided data store,
        verifying CRC for data integrity.

        Args:
            data_store: The data store object to interact with.

        Raises:
            CRCError: If the CRC checksum of a line doesn't match the calculated value.
        """
        with open(self.log_file.name, "r") as log_file:
            for line in log_file:
                elements = line.strip().split(self.separator)
                crc_value_str = elements[0]
                crc_value = int(crc_value_str)

                data_string = self.separator.join(elements[1:])
                calculated_crc = calculate_crc(data_string)
                if calculated_crc != crc_value:
                    print(f"CRC mismatch at line: {line}")
                    break

                # Extract operation and data from the data string
                operation_str, key, *data = data_string.split(self.separator)
                processed_operation_str = operation_str.strip().lower()
                operation = SupportedCommands(processed_operation_str)
                entry = {"key": key}
                if processed_operation_str in ["set","setnx","setxx","getdel","del"] :
                    for i in data:
                        if i in ["nx","px","ex","xx"]:
                            # check if it' options or what?
                            entry["options"] = Options(i)   # TODO: handle for multiple options in future.
                        elif isinstance(i, int):
                            entry["ttl"] = int(i)
                        else:
                            entry["value"] = i
                
                if operation.value.strip().lower() in [SupportedCommands.SET.value, SupportedCommands.SETNX.value,SupportedCommands.SETXX.value,SupportedCommands.GETDEL.value]:
                    commands = [operation.value.strip().lower(),entry["key"],]
                    if "value" in entry:
                        commands.append(entry["value"])
                    if "options" in entry:
                        if entry["options"].value == Options.EX or entry["options"].value == Options.PX:
                            commands.append(entry["options"])
                            commands.append(entry["ttl"])
                        else:
                            commands.append(entry["options"].value)
                    command_handler.handle(commands)
            
    def clear(self) -> None:
        """Clears the contents of the AOF file."""
        self.log_file.truncate(0)
        self.log_file.seek(0)
