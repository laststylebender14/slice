import socket
import selectors

from core.logger import logger
from core.server.iserver import IServer
from core.storage import KVStore, IStore
from core.iomultiplexing import IO_Multiplexer
from core.resp import decode_redis_command
from core.commandhandler import CommandHandler
from core.resp import encode_bulk_strings_reps
from core.expiration import delete_expired_keys


class Server(IServer):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        store: IStore = KVStore(),
        command_handler: CommandHandler = None,
    ) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(20_000)
        self.server_socket.setblocking(False)

        self.store = store
        # instantiate command_handler to understand resp and forward it to appropriate handler
        self.command_handler = command_handler

        # instantiate the io multiplexer
        self.io_multiplexer = IO_Multiplexer(
            selector=selectors.DefaultSelector(),
            server_socket=self.server_socket,
            server=self,
        )
        logger.info(f"Dice DB started at {host}:{port}")

    def start_server(self):
        """
        start io multiplexer for listening in-coming requests.
        """
        self.io_multiplexer.run()

    def cron_execution(self):
        storage_layer = self.store.store
        """ 
            TODO: move below call to separate thread as when more entires are expired then below funtion call blocks main thread for clean-up.
            think about moving below function call to separate thread, 
            but for that necesary locking mechanims needs to be implemented on data store.
        """
        delete_expired_keys(storage_layer)

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
