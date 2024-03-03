import selectors
import socket
from time import time

from core.server.iserver import IServer
from core.logger.logger import get_logger


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
        get_logger().info(f"i/o multiplexer registered with server socket")

    def accept(self, client_socket: socket.socket, mask):
        conn, addr = client_socket.accept()
        self.concurrent_connection_count += 1
        get_logger().info(
            f"Accepted connection from {addr}, total connection count : {self.concurrent_connection_count}"
        )
        conn.setblocking(False)
        self.selector.register(conn, selectors.EVENT_READ, self.handle_connection)

    def handle_connection(self, client_socket: socket.socket, mask):
        data = client_socket.recv(1024).decode().strip()
        if not data:
            self.concurrent_connection_count -= 1
            get_logger().info(
                f"connection terminated from {client_socket}, total connection count : {self.concurrent_connection_count}"
            )
            self.selector.unregister(client_socket)
            client_socket.close()
        else:
            self.server.handle_connection(client_socket=client_socket, data=data)

    def run(self):
        last_cron_exec_time = time()

        while True:
            if time() - last_cron_exec_time >= self.cron_frequency:
                self.server.cron_execution()
                last_cron_exec_time = time()
                pass
            events = self.selector.select(-1)
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

    def __del__(self):
        """
        clean up for the selectors
        """
        self.selector.unregister(self.server_socket)
