import UDPClient

client = UDPClient.UDPClient()
client.connect("localhost",9999)
while True:
    msg = input("Enter what to send: ")
    client.send(msg)
