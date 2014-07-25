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
        self.mydots.set_colorkey((0,0,0))
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
                    print(xy.tostring())
                    self.send(xy.tostring())


    def get_idot(self, xy):
        pyg.draw.circle(self.idots, (255, 255, 255), xy, 10, 0)
        self.update()

    def update(self):
        self.screen.blit(self.idots, (0,0))
        self.screen.blit(self.mydots, (0,0))
        pyg.display.update()

class PygameHandler(socketserver.BaseRequestHandler):
    def handle(self):
        #temp jank parsing
        data = self.request[0][-8:]
        print(data)
        xy= np.fromstring(data, dtype=int)
        print(data, xy)

        self.server.get_idot(xy)

if __name__ == "__main__":
    cl = PygameClient(("0.0.0.0",12801), PygameHandler)
    cl.connect("184.66.98.2", 12800)
    cl.run()
    cl.loop()
