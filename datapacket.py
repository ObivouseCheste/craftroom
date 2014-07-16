

class DataPacket():
    def __init__(self, msg, seq=None, ack=None, vital=False, preserialized=False):
        #self.data += "{0:b}".format(seq) + DataPacket.programID() + msg
        self.serialized = False
        if preserialized:
            self.data = "CMRM " + str(seq) + " " + str(ack) + " "
            self.data = self.serialize()
            self.data += msg
            self.serialized = True
        else:
            self.data = "CMRM " + str(seq) + " " + str(ack) + " " + msg
        print(self.data)
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
    def deserialize(msg):
        ds = msg.decode("UTF-8")
        words = ds.split()
        return DataPacket(" ".join(words[3:]), words[1], words[2])
