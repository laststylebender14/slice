from dotenv import load_dotenv
import os

from core.logger import set_logging_level
from config.wal_config import WalConfig
from config.server_config import ServerConfig


def load_config():
    load_dotenv()
    set_logging_level(os.getenv("LOGGING_LEVEL", "info"))

    WalConfig().set_wal_enable(os.getenv("ENABLE_PERSISTENCE", False))
    WalConfig().set_path(os.getenv("WAL_FILE_PATH", "./aof.slice"))
    ServerConfig().set_host(os.getenv("HOST", "localhost"))
    ServerConfig().set_port(os.getenv("PORT", 6379))
