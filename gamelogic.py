import numpy as np
import collide
import pyglet
from lobby import Lobby, LobbyHandler
from pyglet.window import key

class World:
    def __init__(self):
        #maybe should be using sparse matrix
        self.keyobjs = {}
        self.objects = set()



class WorldObject(pyglet.sprite.Sprite):
    def __init__(self, image, x, y, **kwargs):
            pyglet.sprite.Sprite.__init__(self, image, x, y, **kwargs)
            self.col = collide.SpriteCollision(self)
            self.rect = collide.Rect.from_sprite(self)


class SpaceLobby(Lobby):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tile = pyglet.image.load("block.png")
        self.world = World()

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

    def place_tile(self, x, y):
        self.world.objects += WorldObject(self.tile, x, y)

    def dist_squared(self, obj, x, y):
        return (obj.x - x)**2 + (obj.y - y)**2

    def on_mouse_press(self, x, y, button, modifiers):
        if self.me.dist_squared(x, y) < 900:
            self.place_tile(x, y)

if __name__ == "__main__":
    window = Lobby(("0.0.0.0", 12801), LobbyHandler)
    window.connect("184.66.98.2", 12800)
    window.run()
    pyglet.app.run()