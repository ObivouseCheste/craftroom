import numpy as np
import collide
import pyglet
from lobby import Lobby, LobbyHandler
from pyglet.window import key
import random

class World:
    def __init__(self):
        #maybe should be using sparse matrix
        self.keyobjs = {}
        self.objs = set()



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
        self.icon = pyglet.image.load("sprite.png")
        self.world.keyobjs['me'] = self.__class__.create_sprite(img=self.icon)
        self.me = self.world.keyobjs['me']

    def connect_client(self, msg):
        self.world.keyobjs[msg.uid] = self.__class__.create_sprite(img=self.icon, red=msg.msg[0], green=msg.msg[1],
                                                                blue=msg.msg[2])

    def logic(self, dt):
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

            self.send(np.array([self.objects['me'].x, self.objects['me'].y]).tostring(), uid=self.uid)

    def draw_world(self):
        self.world.keyobjs['me'].draw()
        for sprite in self.world.keyobjs.values():
            sprite.draw()
        for sprite in self.world.objects:
            sprite.draw()

    def place_tile(self, x, y):
        self.world.objects += WorldObject(self.tile, x, y)

    def dist_squared(self, obj, x, y):
        return (obj.x - x)**2 + (obj.y - y)**2

    def on_mouse_press(self, x, y, button, modifiers):
        if self.dist_squared(self.me, x, y) < 900:
            self.place_tile(x, y)
            
    @staticmethod
    def create_sprite(red=None, green=None, blue=None, x=50, y=50, img=None):
        if red is None:
            red = random.randint(0, 255)
        if green is None:
            green = random.randint(0, 255)
        if blue is None:
            blue = random.randint(0, 255)
        sprite = pyglet.sprite.Sprite(img, x, y)
        sprite.color = (red, green, blue)
        return sprite

if __name__ == "__main__":
    window = SpaceLobby(("0.0.0.0", 12801), LobbyHandler)
    window.connect("184.66.98.2", 12800)
    window.run()
    pyglet.app.run()