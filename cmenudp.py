import socket
import socketserver
import threading
import datapacket

class CmenServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    ''' Has a set of connections '''
    def run(self):
        self.server_thread = threading.Thread(target = self.serve_forever)
        self.server_thread.daemon = False #exit when main thread exits?
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

    def send(self, msg, vital=False, msg_hash=0x00, uid=0):
        data = datapacket.DataPacket(msg, msg_hash=msg_hash, vital=vital, uid=uid)
        self.localseq += 1
        self.socket.sendto(data.data,(self.ip, self.port))
        print(data.data)

class FwdServer(CmenServer):
    def __init__(self, *args, **kwargs):
        self.connections = dict()
        self.connectioncolors = dict()
        self.lastconnection = -1
        super().__init__(*args, **kwargs)

class FwdHandler(socketserver.BaseRequestHandler):
    ''' Forwards all messages sent to all connected '''

    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        addr = (self.client_address[0], self.client_address[1])
        dsdata = datapacket.DataPacket.deserialize(data)

        is_connect_request = True if dsdata.msg_hash == b'\xb6@\xa0' else False

        if addr not in self.server.connections.values():
            self.server.lastconnection += 1
            self.server.connections[self.server.lastconnection] = addr
            self.server.connectioncolors[self.server.lastconnection] = (dsdata.msg[0], dsdata.msg[1], dsdata.msg[2])
            print(self.server.connections)

        for cid, client in self.server.connections.items():
            if is_connect_request:
                specialdata = datapacket.DataPacket(msg=dsdata.msg, msg_hash=dsdata.msg_hash, ack=dsdata.ack,
                                                    seq=dsdata.seq, uid=self.server.lastconnection % 256)
                socket.sendto(specialdata.data, client)
                # colors = self.server.connectioncolors[cid]
                # connecteduser = datapacket.DataPacket(msg=bytes([colors[0], colors[1], colors[2]]), ack=dsdata.ack,
                #                                       seq=dsdata.seq, msg_hash=dsdata.msg_hash, uid=cid % 256)
                # socket.sendto(connecteduser.data, addr)
            else:
                socket.sendto(data, client)

if __name__ == "__main__":
    serv = FwdServer(("0.0.0.0",12800), FwdHandler)
    serv.run()
