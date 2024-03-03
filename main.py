from core.server.server import Server
from core.storage.kv_store import KVStore
from core.aof.aof import AOF_V2
from core.commandhandler.command_handler import CommandHandler


banner = """ 
 ____  _ _            ____  ____  
/ ___|| (_) ___ ___  |  _ \| __ ) 
\___ \| | |/ __/ _ \ | | | |  _ \ 
 ___) | | | (_|  __/ | |_| | |_) |
|____/|_|_|\___\___| |____/|____/ 
"""

if __name__ == "__main__":
    walFile = None
    if False:
        # TODO: enalbe via configuration.
        walFile = AOF_V2("./aof.slice",)
    store = KVStore()
    if walFile:
        print("[Logger]:","Checking for AOF file")
        print("[Logger]:","Replying the for AOF file")
        walFile.replay(CommandHandler(store=store, walFile=None))
        print("[Logger]:","Replying the for AOF file done")
    command_handler = CommandHandler(store=store, walFile=walFile)
    print(banner)
    banner = None # clean-up allocated memeory for banner
    Server(store=store,command_handler=command_handler).start_server()
    