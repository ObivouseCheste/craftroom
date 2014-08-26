import pyglet
from pyglet.window import key
import random
import cmenudp
import socketserver
import numpy as np
import queue
import datapacket
import hashlib


class Lobby(cmenudp.CmenClient, pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        cmenudp.CmenClient.__init__(self, *args, **kwargs)
        pyglet.window.Window.__init__(self)
        pyglet.clock.schedule_interval(self.update, 1 / 60)
        self.fps_display = pyglet.clock.ClockDisplay()
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)

        self.sq = queue.Queue()
        self.cconfirmed = False
        self.connectseed = bytes([random.randrange(256),random.randrange(256)])
        self.connecting_label = pyglet.text.Label('Connecting..', font_name='Times New Roman', font_size=36,
                                                  x=self.width // 2, y=self.height // 2, anchor_x='center',
                                                  anchor_y='center')
        self.uid = 0
        self.time_since_attempt = 0
        self.event_dict, self.hash_dict = self.build_event_dict()

    def build_event_dict(self):
        '''
        :returns:
        '''
        event_dict = {}
        hash_dict = {}
        print("Building event dict")
        for attr in dir(self):
            if attr[:6] == "event_":
                print(attr)
                method = getattr(self, attr)
                ack = None
                if hasattr(self, "ack_"+attr[6:]):
                    ack = getattr(self, "ack_"+attr[6:])
                if callable(method):
                    m = hashlib.md5()
                    m.update(attr[6:].encode("UTF-8"))
                    h = m.digest()[:3]
                    if h in event_dict:
                        raise ValueError("HASH COLLISION: %s AND %s", (attr, event_dict[h]))
                    else:
                        print("Assigned " + str(h) + " to " + attr)
                        if b'\xb6@\xa0' == h:
                            print(True)
                        hash_dict[attr[6:]] = h
                        event_dict[h] = (method, ack)
        return event_dict, hash_dict

    def update(self, dt):
        for msg in self.received():
            event = self.event_dict[msg.msg_hash]
            event(msg)


        if self.cconfirmed:
            self.logic(dt)
    
        else:
            self.time_since_attempt += dt
            if self.time_since_attempt >= 1:
                self.time_since_attempt = 0
                # self.send(self.connectseed, connectTransaction=True)
                self.attempt_connection()

    def attempt_connection(self):
        msg = bytearray()
        for seed in self.connectseed:
            msg += seed
        self.send(msg=msg, msg_hash=self.hash_dict["connect"])

    def event_connect(self, msg):
        if not self.cconfirmed and msg.msg == self.connectseed:
            self.uid = msg.uid
            print(msg.uid)
            self.cconfirmed = True
            print("Got one")
        elif msg.msg != self.connectseed:
            print("Created:")
            print(msg.uid)
            self.connect_client(msg)

    def connect_client(self, msg):
        pass
   
    def logic(self, dt):
        pass

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
    

class LobbyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        self.server.sq.put(datapacket.DataPacket.deserialize(data))


if __name__ == "__main__":
    window = Lobby(("0.0.0.0", 12801), LobbyHandler)
    window.connect("184.66.98.2", 12800)
    window.run()
    pyglet.app.run()