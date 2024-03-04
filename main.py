from core.logger.logger import logger
from core.server.server import Server
from core.storage.kv_store import KVStore
from core.aof.aof import AOF_V2
from core.commandhandler.command_handler import CommandHandler
from config import load_config, WalConfig, ServerConfig


banner = """ 
 ____  _ _            ____  ____  
/ ___|| (_) ___ ___  |  _ \| __ ) 
\___ \| | |/ __/ _ \ | | | |  _ \ 
 ___) | | | (_|  __/ | |_| | |_) |
|____/|_|_|\___\___| |____/|____/ 
"""

if __name__ == "__main__":
    load_config()

    walFile = None
    if WalConfig().is_wal_enabled():
        walFile = AOF_V2(WalConfig().get_path())
    store = KVStore()
    if walFile:
        logger.info("Checking for AOF file")
        logger.info("Replying the for AOF file")
        walFile.replay(CommandHandler(store=store, walFile=None))
        logger.info("Replying the for AOF file done")
    command_handler = CommandHandler(store=store, walFile=walFile)
    print(banner)
    banner = None  # clean-up allocated memeory for banner
    Server(
        host=ServerConfig().get_host(),
        port=ServerConfig().get_port(),
        store=store,
        command_handler=command_handler,
    ).start_server()
