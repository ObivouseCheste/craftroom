

class DataPacket():
    def __init__(self, msg, seq, ack, vital=False):
        #self.data += "{0:b}".format(seq) + DataPacket.programID() + msg
        self.data = "CMRM " + str(seq) + " " + str(ack) + " " + msg
        self.vital = vital
        self.msg = msg
        self.seq = seq
        self.ack = ack

    def isVital(self):
        return self.vital

    def getMessage(self):
        return self.msg

    def getSequenceNum(self):
        return self.seq

    def getAck(self):
        return self.ack

    def getData(self):
        return self.data

    def serialize(self):
        return self.data.encode("UTF-8")

    @classmethod
    def deserialize(msg)
        ds = msg.decode("UTF-8")
        words = ds.split()
        return DataPacket(" ".join(words[3:]), words[1], words[2])
