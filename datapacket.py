

class DataPacket():
    def __init__(self, msg, seq=0, ack=0, vital=False, preserialized=False, connectTransaction = False, uid=0):
        #self.data += "{0:b}".format(seq) + DataPacket.programID() + msg
        self.data = bytearray()
        self.data.extend(b'CMRM')
        self.data.append(0x00 if not connectTransaction else 0x01)
        self.data.append(0x00)
        self.data.append(uid % 256)
        #for future use
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
        self.connectTransaction = connectTransaction
        self.uid = uid

    def serialize(self):
        if not self.serialized:
            return self.data.encode("UTF-8")
        else:
            return self.data

    @classmethod
    def deserialize(cls, msg):
        """

        :rtype : datapacket.DataPacket
        """
        return cls(msg[9:],msg[7],msg[8], connectTransaction = True if msg[4] == 0x01 else False,
                   preserialized = True, uid=msg[6])
