import pygame as pyg
import cmenudp
import numpy as np

import socket
import socketserver
import threading
import datapacket

class PygameClient(cmenudp.CmenClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen = pyg.display.set_mode((500,500))
        self.mydots = pyg.Surface((500,500))
        self.idots = pyg.Surface((500,500))

    def loop(self):
        while True:
            for evt in pyg.event.get():
                if evt.type == pyg.QUIT:
                    pyg.quit()
                    sys.exit()
                if evt.type == pyg.MOUSEBUTTONDOWN:
                    xy = np.array(evt.pos)
                    pyg.draw.circle(self.mydots, (255, 0, 0), xy, 5, 0)
                    self.update()

                    self.send(xy.tostring())


    def get_idot(xy):
        pyg.draw.circle(self.mydots, (255, 255, 255), xy, 10, 0)
        self.update()

    def update(self):
        self.screen.blit(self.idots, (0,0))
        print(self.server_address)
        #self.screen.blit(self.mydots, (0,0))
        pyg.display.update()

class PygameHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        #msg = datapacket.DataPacket.deserialize(data).msg
        xy= np.fromstring(data)

        self.server.get_idot(xy)
        print(self.client_address[0])
        print(xy)

if __name__ == "__main__":
    cl = PygameClient(("localhost",12801), PygameHandler)
    cl.connect("localhost", 12800)
    cl.run()
    cl.loop()
