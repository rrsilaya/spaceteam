from socket import AF_INET, socket, SOCK_DGRAM
HOST = 'localhost'
TCP_PORT = 80
UDP_PORT = 3003
BUFFER = 4096

Message = "Hello server"
encodedMessage = str.encode(Message)
_socket = socket(AF_INET, SOCK_DGRAM)

_socket.sendto(encodedMessage, (HOST, UDP_PORT))

msgFromServer = _socket.recvfrom(BUFFER)

 

msg = "Message from Server {}".format(msgFromServer[0])

print(msg)