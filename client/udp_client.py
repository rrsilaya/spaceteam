from socket import AF_INET, socket, SOCK_DGRAM
HOST = 'localhost'
TCP_PORT = 80
UDP_PORT = 3003
BUFFER = 4096

class UDPClient():
	def __init__(self):
		self.address = (HOST, UDP_PORT)
		self._socket = socket(AF_INET, SOCK_DGRAM)
		self._socket.connect(self.address)

	def send(self,data):
		encodedMessage = str.encode(data)
		self._socket.sendto(encodedMessage, self.address)
		msg = self.receive()
		print(msg)
	def receive(self):
		msgFromServer = self._socket.recvfrom(BUFFER)
		return msgFromServer
 

#msg = "Message from Server {}".format(msgFromServer[0])
if __name__ == "__main__":
	client = UDPClient()
	while (True):
		message = input(">game:	")
		client.send(message)
		if message == "q":
			break
