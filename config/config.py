from dotenv import load_dotenv
import os

from core.logger import set_logging_level, logger
from config.wal_config import WalConfig
from config.server_config import ServerConfig


def load_config():
    load_dotenv()
    set_logging_level(os.getenv("LOGGING_LEVEL", "info"))

    WalConfig().wal_enable = os.getenv("ENABLE_PERSISTENCE", False)
    if WalConfig().wal_enable:
        WalConfig().path = os.getenv("WAL_FILE_PATH", "./aof.slice")
        WalConfig.flush_frequency = os.getenv("FLUSH_FREQUENCY", 1000)
    
    ServerConfig().host = (os.getenv("HOST", "localhost"))
    ServerConfig().port = (os.getenv("PORT", 6379))

    logger.info("All Configurations are loaded.")
    logger.info(f"WalConfig: {WalConfig()} ")
    logger.info(f"ServerConfig: {ServerConfig()} ")
    