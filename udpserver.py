import socket
import socketserver
import threading
import datapacket

class UDPServer:
    def __init__(self):
        self.server = ""

    class ThreadedUDPHandler(socketserver.BaseRequestHandler):
        def __init__(self, *args, **kwargs):
            self.connections = set()
            super().__init__(*args, **kwargs)

        def handle(self):
            data = datapacket.DataPacket.deserialize(self.request[0])
            socket = self.request[1]

            addr = self.client_address
            msg = data.getMessage().split()

            if addr not in self.connections:
                self.connections.add(addr)

            #error handling

            send = " ".join(msg).encode("UTF-8")

            for client in self.connections:
                socket.sendto(send, addr)

            print("{} wrote:".format(self.client_address[0]))
            print(data)
            #socket.sendto(data.upper().encode('UTF-8'), self.client_address)

    class ThreadingUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer): pass

    def run(self):
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
