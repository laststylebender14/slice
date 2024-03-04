import selectors
import socket
from time import time

from core.logger import logger
from core.server.iserver import IServer


class IO_Multiplexer:
    def __init__(
        self,
        selector: selectors.BaseSelector,
        server_socket: socket.socket,
        server: IServer,
    ):
        self.selector = selector
        self.server = server
        self.server_socket = server_socket
        self.concurrent_connection_count = 0
        self.selector.register(server_socket, selectors.EVENT_READ, self.accept)

        self.cron_frequency = 1
        logger.info(f"i/o multiplexer registered with server socket")

    def accept(self, client_socket: socket.socket, mask):
        conn, addr = client_socket.accept()
        self.concurrent_connection_count += 1
        logger.info(
            f"Accepted connection from {addr}, total connection count : {self.concurrent_connection_count}"
        )
        conn.setblocking(False)
        self.selector.register(conn, selectors.EVENT_READ, self.handle_connection)

    def handle_connection(self, client_socket: socket.socket, mask):
        data = client_socket.recv(1024).decode().strip()
        if not data:
            self.concurrent_connection_count -= 1
            logger.info(
                f"connection terminated from {client_socket}, total connection count : {self.concurrent_connection_count}"
            )
            self.selector.unregister(client_socket)
            client_socket.close()
        else:
            self.server.handle_connection(client_socket=client_socket, data=data)

    def run(self):
        last_cron_exec_time = time()
        try:
            while True:
                if time() - last_cron_exec_time >= self.cron_frequency:
                    self.server.cron_execution()
                    last_cron_exec_time = time()
                    pass
                events = self.selector.select(-1)
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)
        except OSError as e:
            logger.error(f"OSError {e}")
        except KeyboardInterrupt:
            logger.error(f"Keyboard interrupt detected.")
        except Exception as e:
            logger.error(f"Exception occurred. {e}")
        finally:
            logger.error(f"closing server socket.")
            self.server_socket.close()
            self.selector.unregister(self.server_socket)
            
