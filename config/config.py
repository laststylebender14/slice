from dotenv import load_dotenv
import os

from core.logger import set_logging_level, logger
from config.wal_config import WalConfig
from config.server_config import ServerConfig


def load_config():
    load_dotenv()
    set_logging_level(os.getenv("LOGGING_LEVEL", "info"))

    wal_instance = WalConfig()
    wal_instance.wal_enable = os.getenv("ENABLE_PERSISTENCE", False)
    if wal_instance.wal_enable:
        wal_instance.path = os.getenv("WAL_FILE_PATH", "./aof.slice")
        wal_instance.flush_frequency = os.getenv("FLUSH_FREQUENCY", "1000")
        wal_instance.ttl_normalizer = os.getenv("TTL_NORMALIZER", "1709618598664")
    
    server_instance = ServerConfig()
    server_instance.host = os.getenv("HOST", "localhost")
    server_instance.port = os.getenv("PORT", 6379)

    logger.info("All Configurations are loaded.")
    logger.info(f"WalConfig: {wal_instance}")
    logger.info(f"ServerConfig: {server_instance}")
    