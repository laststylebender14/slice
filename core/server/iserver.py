from abc import ABC, abstractmethod
import socket

class IServer(ABC):
    def __init__(self,host:str="localhost",port:int=6379) -> None:
        pass
    @abstractmethod
    def handle_connection(self, client_socket: socket.socket,data: any):
        pass
    
    @abstractmethod
    def start_server(self):
        pass
    
    @abstractmethod
    def cron_execution(self):
        pass