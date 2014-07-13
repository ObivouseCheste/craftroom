import UDPClient

client = UDPClient.UDPClient()
client.connect("127.0.0.0",555)
client.send("Hello")
