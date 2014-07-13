

class DataPacket():
    def __init__(self, msg, seq, ack, vital=False):
        #self.data += "{0:b}".format(seq) + DataPacket.programID() + msg
        self.data = str(seq) + " " + str(ack) + " " + msg
        self.vital = vital
        self.msg = msg
        self.seq = seq
        self.ack = ack

    def isVital(self):
        return self.vital

    def message(self):
        return self.msg

    def sequenceNum(self):
        return self.seq

    def getAck(self):
        return self.ack

    def getData(self):
        return self.data
