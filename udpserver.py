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

            addr = self.client_address
            msg = data.split()

            if addr not in self.connections:
                self.connections.add(addr)

            #error handling

            for client in self.connections:
                socket.sendto(msg[2:], addr)

            print("{} wrote:".format(self.client_address[0]))
            print(data)
            #socket.sendto(data.upper().encode('UTF-8'), self.client_address)

    class ThreadingUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer): pass

    def go(self):
        self.server = self.ThreadingUDPServer(("0.0.0.0",12800), self.ThreadedUDPHandler)
        server_thread = threading.Thread(target = self.server.serve_forever)
        server_thread.daemon = True #exit when main thread exits?
        server_thread.start()
        print(self.server.server_address)

    def connect_client(self, client):
        if type(client) is UDPClient:
            self.connections.add(client)

    def disconnect_client(self, client):
        if client in self.connections:
            self.connections.remove(client)
