from abc import ABC, abstractmethod
import socket

class IServer(ABC):
    @abstractmethod
    def handle_connection(self, client_socket: socket.socket, data: any):
        pass

    @abstractmethod
    def start_server(self):
        pass

    @abstractmethod
    def cron_execution(self):
        pass
