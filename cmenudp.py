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
        self.localseq = 0
        self.remoteseq = 0

    def connect(self, ip, port):
        if not self.connected:
            self.ip = ip
            self.port = port
            self.connected = True
        else:
            return False

    def send(self, msg, vital=False, connectTransaction=False, uid=0):
        if type(msg) == bytes:
            ps = True
        print(connectTransaction)
        data = datapacket.DataPacket(msg, preserialized=ps, connectTransaction=connectTransaction, uid=uid)
        self.localseq += 1
        self.socket.sendto(data.serialize(),(self.ip,self.port))

class FwdServer(CmenServer):
    def __init__(self, *args, **kwargs):
        self.connections = dict()
        self.lastconnection = -1
        super().__init__(*args, **kwargs)

class FwdHandler(socketserver.BaseRequestHandler):
    ''' Forwards all messages sent to all connected '''

    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        addr = (self.client_address[0], self.client_address[1])
        dsdata = datapacket.DataPacket.deserialize(data)

        connectrequest = True if data[4] == 0x01 else False

        if addr not in self.server.connections.values():
            self.server.lastconnection += 1
            self.server.connections[self.server.lastconnection] = addr
            print(self.server.connections)

        for cid, client in self.server.connections.items():
            if connectrequest:
                specialdata = datapacket.DataPacket(dsdata.msg, dsdata.ack, dsdata.seq,
                connectTransaction = True, uid=self.server.lastconnection % 256, preserialized=True)
                socket.sendto(specialdata.serialize(), client)
            else:
                socket.sendto(data, client)

if __name__ == "__main__":
    serv = FwdServer(("0.0.0.0",12800), FwdHandler)
    serv.run()
