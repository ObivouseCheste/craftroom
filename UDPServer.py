import socket
import socketserver
import threading

class UDPServer:
    def __init__(self):
        self.connections = set()
        self.server = ""

    class ThreadedUDPHandler(socketserver.BaseRequestHandler):
        def handle(self):
            data = self.request[0].strip()
            socket = self.request[1]

            print("{} wrote:".format(self.client_address[0]))
            print(data)
            socket.sendto(data.upper().encode('UTF-8'), self.client_address)

    class ThreadingUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer): pass

    def go(self):
        self.server = self.ThreadingUDPServer(("localhost",9999), self.ThreadedUDPHandler)
        server_thread = threading.Thread(target = self.server.serve_forever)
        server_thread.daemon = True #exit when main thread exits?
        server_thread.start()

    def connect_client(self, client):
        if type(client) is UDPClient:
            self.connections.add(client)

    def disconnect_client(self, client):
        if client in self.connections:
            self.connections.remove(client)
