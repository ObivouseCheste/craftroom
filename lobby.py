import pyglet
from pyglet.window import key
import random
import cmenudp
import socketserver
import numpy as np
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
        self.objects = dict()
        self.objects['me'] = Lobby.create_sprite(img=self.icon)
        self.sq = queue.Queue()
        self.cconfirmed = False
        self.connectseed = bytes([self.objects['me'].color[0], self.objects['me'].color[1], self.objects['me'].color[2]])
        self.connecting_label = pyglet.text.Label('Connecting..', font_name='Times New Roman', font_size=36,
                                                  x=self.width // 2, y=self.height // 2, anchor_x='center',
                                                  anchor_y='center')
        self.uid = 0
        self.time_since_attempt = 0
        self.methoddict = {}

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
                    self.objects[msg.uid] = Lobby.create_sprite(img=self.icon, red=msg.msg[0], green=msg.msg[1],
                                                                blue=msg.msg[2])
            elif msg.uid in self.objects:
                pos = np.fromstring(msg.msg, dtype=float)
                print(pos)
                #print(msg.uid)
                #print(pos)
                self.objects[msg.uid].position = pos

        if self.cconfirmed:
            updated = False
            if self.keys[key.RIGHT]:
                self.objects['me'].x += 80.0 * dt
                updated = True
            if self.keys[key.LEFT]:
                self.objects['me'].x += -80.0 * dt
                updated = True
            if self.keys[key.UP]:
                self.objects['me'].y += 80.0 * dt
                updated = True
            if self.keys[key.DOWN]:
                self.objects['me'].y += -80.0 * dt
                updated = True
            if self.keys[key.SPACE]:
                self.objects['me'].x = 0.0
                self.objects['me'].y = 0.0
                updated = True
            if updated:
                #print(self.objects['me'].position)
                self.send(np.array([self.objects['me'].x, self.objects['me'].y]).tostring(), uid=self.uid)
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
            self.objects['me'].draw()
            for id, sprite in self.objects.items():
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
    def create_sprite(cls, red=None, green=None, blue=None, x=50, y=50, img=None):
        if red is None:
            red = random.randint(0, 255)
        if green is None:
            green = random.randint(0, 255)
        if blue is None:
            blue = random.randint(0, 255)
        sprite = pyglet.sprite.Sprite(img, x, y)
        sprite.color = (red, green, blue)
        return sprite

    def propagated(self, id):
        def propagated_dec(method):
            self.methoddict[id] = method

            def prop_method(instance, *args, **kwargs):
                method(*args, **kwargs)
                instance.send(ENCODETHISSTUFF(id, *args, **kwargs))
            return prop_method
        return propagated_dec

    @propagated("boop")
    def do_boop(self):
        print("BOOOOP")


class LobbyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        self.server.sq.put(datapacket.DataPacket.deserialize(data))


if __name__ == "__main__":
    window = Lobby(("0.0.0.0", 12801), LobbyHandler)
    window.connect("184.66.98.2", 12800)
    window.run()
    pyglet.app.run()