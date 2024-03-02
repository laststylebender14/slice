import socket
import selectors

from core.storage.kv_store import Store
from core.server.iserver import IServer
from core.iomultiplexing.io_multiplexing import IO_Multiplexer
from core.resp.decoder import decode_redis_command
from core.commandhandler.command_handler import CommandHandler
from core.aof.aof import AOF
from core.resp.encoder import encode_simple_strings_resp, encode_bulk_strings_reps,encode_null_string_resp

class Server(IServer):
    def __init__(self,store: Store, host:str="localhost",port:int=6379) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server_socket.bind((host,port))
        self.server_socket.listen(5)
        self.server_socket.setblocking(False)
        
        # instantiate command_handler to understand resp and forward it to appropriate handler
        self.command_handler = CommandHandler(store, walFile=AOF("./aof.slice"))
        
        # instantiate the io multiplexer
        self.io_multiplexer = IO_Multiplexer(selector= selectors.KqueueSelector(), server_socket=self.server_socket, server=self)

    def start_server(self):
        """
            start io multiplexer for listening in-coming requests.
        """
        self.io_multiplexer.run()
        
    def handle_connection(self, client_socket: socket.socket, data: any):
        """ 
            handle connection requests of clients.
        """
        try:
            resp_decoded_req = decode_redis_command(data=data)
            resp = self.command_handler.handle(resp_decoded_req)
            client_socket.send(resp)
        except ValueError as err:
            client_socket.send(encode_bulk_strings_reps(str(err)))