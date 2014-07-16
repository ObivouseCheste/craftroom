import socket
import socketserver
import threading
import datapacket

class CmenServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    ''' Has a set of connections '''
    def run(self):
        self.server_thread = threading.Thread(target = self.serve_forever)
        self.server_thread.daemon = True #exit when main thread exits?
        self.server_thread.start()
        print(self.server_address)

class CmenClient(CmenServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connected = False
        self.ip = "localhost"
        self.port = 12800
        #create a new udp socket
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.localseq = 0
        self.remoteseq = 0

    def connect(self, ip, port):
        if not self.connected:
            self.ip = ip
            self.port = port
            self.connected = True
        else:
            return False

    def send(self, msg, vital=False):
        if type(msg) == bytes:
            ps = True
        data = datapacket.DataPacket(msg, preserialized=ps)
        self.localseq += 1
        self.sock.sendto(data.serialize(),(self.ip,self.port))

class FwdServer(CmenServer):
    def __init__(self, *args, **kwargs):
        self.connections = set()
        super().__init__(*args, **kwargs)

class FwdHandler(socketserver.BaseRequestHandler):
    ''' Forwards all messages sent to all connected '''

    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        addr = self.client_address

        if addr not in self.server.connections:
            self.server.connections.add(addr)

        for client in self.server.connections:
            print(data)
            socket.sendto(data, ("localhost",12801))

        print(self.client_address[0])
        print(self.client_address[1])

if __name__ == "__main__":
    serv = FwdServer(("localhost",12800), FwdHandler)
    serv.run()
