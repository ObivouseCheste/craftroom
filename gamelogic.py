import numpy as np
from lobby import Lobby

class World():
    def __init__(self, x=80, y=60):
        self.world = [[None for _ in range(y)] for _ in range(x)]
        self.objects = {}

    def __getitem__(self, item):
        return self.world[item]

    def get_collsion(self):
        col = np.array([[each.col for each in row] for row in self.world])
        return col


class WorldObject():
    def __init__(self, c=0):
        self.collision = c


class SpaceLobby(Lobby):
    def __init__(self, x=800, y=600, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.world = World(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        pass
