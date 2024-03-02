""" 
TODO: combine io_multiplexer with command handler module.   -> done
TODO: integrate WAL with command handler.                   -> working
TODO: implement key expiry sampler                          -> pending
---------------------------
TODO: add test coverage.                                    -> pending
TODO: integrate RDB file with command handler.              -> pending
TODO: understand different variations of io/multiplexer.    -> pending
"""

from core.server.server import Server
from core.storage.kv_store import KVStore
from core.aof.aof import AOF

Server(store=KVStore()).start_server()

# AOF("./aof.slice").replay()
