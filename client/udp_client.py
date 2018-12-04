from socket import AF_INET, socket, SOCK_DGRAM

from proto.udp_packet_pb2 import UdpPacket

HOST = 'localhost'
TCP_PORT = 80
UDP_PORT = 3003
BUFFER = 4096

class UDPClient():
	def __init__(self):
		self.address = (HOST, UDP_PORT)
		self._socket = socket(AF_INET, SOCK_DGRAM)
		self._socket.connect(self.address)
		
		self.packet = UdpPacket()

	def send(self,data):
		self._socket.sendto(encodedMessage, self.address)

	def receive(self):
		msgFromServer = self._socket.recvfrom(BUFFER)
		return msgFromServer

	def connect(self, playerName):
		payload = self.packet.ConnectPacket()
		payload.type = self.packet.CONNECT 
		payload.player.name = playerName

		self.user = payload.player.name
		payload = payload.SerializeToString()

		self._socket.send(payload)	
	
	def createRoom(self,roomId, maxPlayers):
		payload = self.packet.CreateRoomPacket()
		payload.type = self.packet.CREATE_ROOM
		payload.room_id = roomId
		payload.max_players = maxPlayers
		payload.player.name = self.user

		payload = payload.SerializeToString()
		self._socket.send(payload)
		

	'''
	def join():
		return 0

	def leave():
		return 0
	
	def getPlayers():
		return 0
		msgFromServer = self._socket.recvfrom(BUFFER)
 '''

if __name__ == "__main__":
	client = UDPClient()
	message = input(">name:	")
	client.connect(message)
	while (True):
		message = input("> ")
		if message == "create room":
			roomId = input(">roomId: ")
			maxPlayers = 3
			client.createRoom(roomId,maxPlayers)
			
