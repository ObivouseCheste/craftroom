import pygame as pyg
from udpclient import UDPClient

class PygameClient(UDPClient):
    def __init__(self):
        super().__init__()
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
                    xy = evt.pos
                    pyg.draw.circle(self.mydots, (255, 0, 0), xy, 5, 0)
                    self.update()
                    self.send(str(xy[0]) + " " + str(xy[1]))

    def get_idot(xy):
        pyg.draw.circle(self.mydots, (255, 255, 255), xy, 10, 0)
        self.update()

    def update(self):
        self.screen.blit(self.idots, (0,0))
        self.screen.blit(self.mydots, (0,0))
        pyg.display.update()


if __name__ == "__main__":
    PygameClient().loop()
