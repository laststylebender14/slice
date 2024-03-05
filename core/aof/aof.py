from zlib import crc32
from time import time

from core.aof.wal import WAL
from core.logger import logger
from core.utils.time_utils import convert_ms_to_seconds, convert_time_to_ms, de_normalize_ttl
from config import WalConfig

def calculate_crc(data_string: str) -> int:
    """Calculates the CRC32 checksum for the provided data string."""
    return crc32(data_string.encode())

"""
AOF_V2 is implementation of WAL interface.
AOF_V2 logs pairs into wal file in the following format.

AOF_V2 -> only logs successful operations to reduce the size of log file.

eg.
    3101428243,set,new_key-9129,new_value
    CRC,Operation,Key,Value,Options

"""
class AOF_V2(WAL):
    def __init__(self, log_file_path: str, separator: str = ","):
        self.log_file = open(log_file_path, "a")  # Open file for append
        self.separator = separator
        if self.log_file:
            self.key_buffer_cnt = 0

    def log(self, aof_entry: str) -> None:
        if self.log_file:
            aof_entry = aof_entry.lower()
            log_line = f"{calculate_crc(aof_entry)},{aof_entry}\n"
            logger.debug(log_line)
            self.key_buffer_cnt += 1
            self.log_file.write(log_line)
            if self.key_buffer_cnt >= WalConfig().flush_frequency:
                # if we met flush frequency criteria, then flush the buffered pairs to disk.
                self.log_file.flush()
                logger.info("flushed buffered pairs onto the disk")
                self.key_buffer_cnt = 0
            return True
        return False

    def replay(self, command_handler=None) -> None:
        """
        Replays the logged operations from the AOF file into the provided data store,
        verifying CRC for data integrity.

        TODO: CRC checks failed rows are ignored for now but make it configurable in future.
        Args:
            restore_command_handler: that restores AOF_V2 logged rows to appropriate version.
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
                                time_in_ms = convert_time_to_ms()
                                expired_at_ms = de_normalize_ttl(int(commands[index + 1], 10))
                                actual_ttl_ms = expired_at_ms - time_in_ms
                                if actual_ttl_ms < 0:
                                    # no point in parsing as this entry is already expired.
                                    continue
                                commands[index + 1] = str(actual_ttl_ms)  # ttl in ms.
                                is_expiry_processed = True
                        else:
                            index = commands.index("px")
                            if index + 1 < len(commands):
                                time_in_sec = int(time())
                                expired_at_in_sec = convert_ms_to_seconds(de_normalize_ttl(int(commands[index + 1])))
                                actual_ttl_in_sec = expired_at_in_sec - time_in_sec
                                if actual_ttl_in_sec < 0:                                
                                    # no point in parsing as this entry is already expired.
                                    continue
                                commands[index + 1] = str(actual_ttl_in_sec)  # ttl in ms.
                                is_expiry_processed = True
                        if not is_expiry_processed:
                            logger.warn("corrupt entry = {data_string}")
                            continue
                except ValueError as err:
                    logger.error("corrupt entry = {data_string}")
                    continue

                command_handler.handle(commands)
