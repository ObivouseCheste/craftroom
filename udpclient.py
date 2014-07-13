import socket
import datapacket
#import ipaddress

class UDPClient:
    def __init__(self):
        self.connected = False
        self.ip = "0.0.0.0"
        self.port = 0
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

    def send(self, msg, vital=True):
        data = datapacket.DataPacket(msg, self.localseq, self.remoteseq, vital)
        datastr = data.getData().encode('UTF-8')
        self.localseq += 1
        self.sock.sendto(datastr,(self.ip,self.port))
