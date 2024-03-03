from core.server.server import Server
from core.storage.kv_store import KVStore
from core.aof.aof import AOF_V2
from core.commandhandler.command_handler import CommandHandler


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
    Server(store=store,command_handler=command_handler).start_server()
    