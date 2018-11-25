from socket import AF_INET, socket, SOCK_DGRAM

HOST = 'localhost'
TCP_PORT = 80
UDP_PORT = 3003
BUFFER = 4096

_socket = socket(AF_INET, SOCK_DGRAM)
_socket.bind((HOST, UDP_PORT))
while True:
	data, addr = _socket.recvfrom(BUFFER)
	print("Message: ", data)
	_socket.sendto(b"Hello client", addr)