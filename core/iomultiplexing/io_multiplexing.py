import selectors
import socket
from core.server.iserver import IServer

class IO_Multiplexer:
    def __init__(self,selector: selectors.BaseSelector,server_socket: socket.socket, server: IServer):
        self.selector = selector
        self.server = server
        self.server_socket = server_socket
        self.concurrent_connection_count = 0
        self.selector.register(server_socket,selectors.EVENT_READ,self.accept)
        print(f"i/o multiplexer register with server socket")
    
    def accept(self, client_socket: socket.socket, mask):
        conn, addr = client_socket.accept()
        self.concurrent_connection_count += 1
        print(f"Accepted connection from {addr}, total connection count : {self.concurrent_connection_count}")
        conn.setblocking(False)
        self.selector.register(conn, selectors.EVENT_READ, self.handle_connection)
                
    def handle_connection(self,client_socket: socket.socket, mask):
        data = client_socket.recv(1024).decode().strip()
        if not data:
            self.concurrent_connection_count -= 1
            print(f"connection terminated from {client_socket}, total connection count : {self.concurrent_connection_count}")
            self.selector.unregister(client_socket)
            client_socket.close()
        else:
            self.server.handle_connection(client_socket=client_socket,data=data)
    
    def run(self):
        while True:
            events = self.selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
                
    def __del__(self):
        """
            clean up for the selectors
        """
        self.selector.unregister(self.server_socket)