from zlib import crc32
from time import time

from core.aof.wal import WAL
from core.logger import logger
from core.utils.time_utils import convert_ms_to_seconds


def calculate_crc(data_string: str) -> int:
    """Calculates the CRC32 checksum for the provided data string."""
    return crc32(data_string.encode())


class AOF_V2(WAL):
    def __init__(self, log_file_path: str, separator: str = ","):
        self.log_file = open(log_file_path, "a")  # Open file for append
        self.separator = separator

    def log(self, aof_entry: str) -> None:
        if self.log_file:
            aof_entry = aof_entry.lower()
            log_line = f"{calculate_crc(aof_entry)},{aof_entry}\n"
            logger.debug(log_line)
            self.log_file.write(log_line)
            return True
        return False

    def replay(self, command_handler=None) -> None:
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
                    logger.warn("CRC mismatch at line: {line}")
                    break
                commands = data_string.split(",")
                try:
                    is_ex_present = "ex" in commands
                    is_px_present = "px" in commands
                    if is_px_present or is_ex_present:
                        is_expiry_processed = False
                        index = -1
                        if "ex" in commands:
                            index = commands.index("ex")
                            if index + 1 < len(commands):
                                commands[index + 1] = str(
                                    time() - int(commands[index + 1], 10)
                                )  # ttl in ms.
                                is_expiry_processed = True
                        else:
                            index = commands.index("px")
                            if index + 1 < len(commands):
                                new_ttl = int(
                                    time()
                                    - convert_ms_to_seconds(int(commands[index + 1]))
                                )
                                commands[index + 1] = str(new_ttl)  # ttl in ms.
                                is_expiry_processed = True
                        if not is_expiry_processed:
                            logger.warn("corrupt entry = {data_string}")
                            continue
                except ValueError as err:
                    logger.error("corrupt entry = {data_string}")
                    continue

                command_handler.handle(commands)
