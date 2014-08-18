

class DataPacket():
    def __init__(self, msg, seq=0, ack=0, vital=False, msg_hash=bytes([0x00, 0x00]), uid=0):
        #self.data += "{0:b}".format(seq) + DataPacket.programID() + msg
        self.data = bytearray()
        self.data.extend(b'CMRM')
        self.data.extend(msg_hash)
        self.data.append(0x00)
        self.data.append(uid % 256)
        #for future use
        self.data.append(seq % 256)
        self.data.append(ack % 256)
        #self.data.extend()
        self.data += msg
        self.vital = vital
        self.msg = msg
        self.msg_hash = msg_hash
        self.seq = seq
        self.ack = ack
        self.uid = uid

    @classmethod
    def deserialize(cls, msg):
        """

        :rtype : datapacket.DataPacket
        """
        return cls(msg[10:], seq=msg[8], ack=msg[9], msg_hash=msg[4:6], uid=msg[7])
