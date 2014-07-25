# Byte      Use                 Args [byte], (string)
# 0x00      NONE                -
# 0x01      CONNECT             [red], [green], [blue]
# 0x02      PING                unspecified
# 0x03      QUIT                [reason]
msg_types = {
    "NONE":0x00,
    "CONNECT":0x01,
    "PING":0x02,
    "QUIT":0x03
}