from socket import AF_INET, socket, SOCK_DGRAM

HOST = 'localhost'
TCP_PORT = 80
UDP_PORT = 3003
BUFFER = 4096

class UDPServer():
	def __init__(self):
		self.address = (HOST, UDP_PORT)
		self._socket = socket(AF_INET, SOCK_DGRAM)
		self._socket.connect(self.address)

	def run(self):
		self._socket = socket(AF_INET, SOCK_DGRAM)
		self._socket.bind(self.address)
		while True:
			data, addr = self._socket.recvfrom(BUFFER)
			print("Message from", addr, " : ", data)
			msg = "Hello " + str(addr[1])
			encodedMessage = str.encode(msg)
			self._socket.sendto(encodedMessage, addr)


	def stop(self):
		self._socket.close()

if __name__ == "__main__":
	server = UDPServer()
	server.run()