from pythonosc import udp_client

client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
client.send_message("/stimulate", [1, 5, 300])
