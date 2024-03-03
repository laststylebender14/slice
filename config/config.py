from dotenv import load_dotenv
import os

from config.wal_config import WalConfig





def load_config(path: str | None = None):
    load_dotenv()
    WalConfig().set_wal_enable(os.getenv("ENABLE_PERSISTENCE"))
    WalConfig().set_path(os.getenv("WAL_FILE_PATH"))
    print(WalConfig())