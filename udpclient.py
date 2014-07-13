import socket
#import ipaddress

class UDPClient:
  def __init__(self):
    self.connected = False
    self.ip = "0.0.0.0"
    self.port = 0
    #create a new udp socket
    self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

  def connect(self, ip, port):
    if not self.connected:
      self.ip = ip
      self.port = port
      self.connected = True
    else:
      return False

  def send(self,msg):
    self.sock.sendto(msg.encode('UTF-8'),(self.ip,self.port))
