import UDPClient

client = UDPClient.UDPClient()
client.connect("whatever",12800)
while True:
    msg = input("Enter what to send: ")
    client.send(msg)
