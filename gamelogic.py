import numpy as np
from lobby import Lobby

class World():
    def __init__(self, x=80, y=60):
        #maybe should be using sparse matrix
        self.objects = {}

    def __getitem__(self, item):
        return self.objects[item]




class WorldObject():
    def __init__(self, c=0, name=None):
        self.colmap = c
        self.name = name


class SpaceLobby(Lobby):
    def __init__(self, x=800, y=600, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.world = World(x, y)

    def place_tile(self, x, y):
        tilesize = 10
        for xi in range(x-tilesize, x+tilesize):
            for yi in range(y-tilesize, y+tilesize):
                self.world[xi][yi] =



    def dist_squared(self, obj, x, y):
        return (obj.x - x)**2 + (obj.y - y)**2

    def on_mouse_press(self, x, y, button, modifiers):
        if self.me.dist_squared(x, y) > 900:
            pass
