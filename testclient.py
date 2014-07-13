import udpclient

client = udpclient.UDPClient()
client.connect("localhost",12800)
while True:
    msg = input("Enter what to send: ")
    client.send(msg)
