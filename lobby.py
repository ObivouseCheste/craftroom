import pyglet
from pyglet.window import key
import random
import cmenudp
import socketserver
import numpy
import queue
import datapacket


class Lobby(cmenudp.CmenClient, pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        cmenudp.CmenClient.__init__(self, *args, **kwargs)
        pyglet.window.Window.__init__(self)
        pyglet.clock.schedule_interval(self.update, 1 / 60)
        self.fps_display = pyglet.clock.ClockDisplay()
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.icon = pyglet.image.load("sprite.png")
        self.sprites = dict()
        self.sprite = Lobby.create_sprite(img=self.icon)
        self.sq = queue.Queue()
        self.cconfirmed = False
        self.connectseed = bytes([self.sprite.color[0], self.sprite.color[1], self.sprite.color[2]])
        self.connecting_label = pyglet.text.Label('Connecting..', font_name='Times New Roman', font_size=36,
                                                  x=self.width // 2, y=self.height // 2, anchor_x='center',
                                                  anchor_y='center')
        self.uid = 0
        self.time_since_attempt = 0

    def update(self, dt):
        for msg in self.received():
            if msg.connectTransaction:
                if not self.cconfirmed and msg.msg == self.connectseed:
                    self.uid = msg.uid
                    print(msg.uid)
                    self.cconfirmed = True
                    print("Got one")
                elif msg.msg != self.connectseed:
                    print("Created:")
                    print(msg.uid)
                    self.sprites[msg.uid] = Lobby.create_sprite(img=self.icon, red=msg.msg[0], green=msg.msg[1],
                                                                blue=msg.msg[2])
            elif msg.uid in self.sprites:
                pos = numpy.fromstring(msg.msg, dtype=float)
                #print(msg.uid)
                #print(pos)
                self.sprites[msg.uid].position = pos

        if self.cconfirmed:
            updated = False
            if self.keys[key.RIGHT]:
                self.sprite.x += 80.0 * dt
                updated = True
            if self.keys[key.LEFT]:
                self.sprite.x += -80.0 * dt
                updated = True
            if self.keys[key.UP]:
                self.sprite.y += 80.0 * dt
                updated = True
            if self.keys[key.DOWN]:
                self.sprite.y += -80.0 * dt
                updated = True
            if self.keys[key.SPACE]:
                self.sprite.position = (0,0)
                updated = True
            if updated:
                #print(self.sprite.position)
                self.send(numpy.array([self.sprite.x, self.sprite.y]).tostring(), uid=self.uid)
        else:
            self.time_since_attempt += dt
            if self.time_since_attempt >= 1:
                self.time_since_attempt = 0
                self.send(self.connectseed, connectTransaction=True)


    def on_draw(self):
        pyglet.clock.tick()
        self.clear()
        self.fps_display.draw()
        if self.cconfirmed:
            self.sprite.draw()
            for id, sprite in self.sprites.items():
                sprite.draw()
        else:
            self.connecting_label.draw()


    def received(self):
        while True:
            try:
                yield self.sq.get_nowait()
            except queue.Empty:
                break

    @classmethod
    def create_sprite(self, red=None, green=None, blue=None, x=50, y=50, img=None):
        if red == None:
            red = random.randint(0, 255)
        if green == None:
            green = random.randint(0, 255)
        if blue == None:
            blue = random.randint(0, 255)
        sprite = pyglet.sprite.Sprite(img, x, y)
        sprite.color = (red, green, blue)
        return sprite


class LobbyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        self.server.sq.put(datapacket.DataPacket.deserialize(data))


if __name__ == "__main__":
    window = Lobby(("0.0.0.0", 12802), LobbyHandler)
    window.connect("184.66.98.2", 12800)
    window.run()
    pyglet.app.run()