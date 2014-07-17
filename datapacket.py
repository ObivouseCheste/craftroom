

class DataPacket():
    def __init__(self, msg, seq=0, ack=0, vital=False, preserialized=False):
        #self.data += "{0:b}".format(seq) + DataPacket.programID() + msg
        self.data = bytearray()
        self.data.extend(b'CMRM')
        self.data.extend((0x00,0x00,0x00)) #for future use
        self.data.append(seq % 256)
        self.data.append(ack % 256)
        #self.data.extend()
        self.serialized = False
        if preserialized:
            self.data += msg
            self.serialized = True
        else:
            self.data.extend(msg.encode("UTF-8"))
            self.serialized = True
        self.vital = vital
        self.msg = msg
        self.seq = seq
        self.ack = ack

    def serialize(self):
        if not self.serialized:
            return self.data.encode("UTF-8")
        else:
            return self.data

    @classmethod
    def deserialize(cls, msg):
        ds = msg.decode("UTF-8")
        words = ds.split()
        return cls(" ".join(words[3:]), words[1], words[2])
