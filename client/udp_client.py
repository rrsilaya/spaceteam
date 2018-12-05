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
		self._socket.sendto(data, self.address) 

	def connect(self, playerName):
		payload = self.packet.ConnectPacket()
		payload.type = self.packet.CONNECT 
		payload.player.name = playerName

		self.user = payload.player.name
		payload = payload.SerializeToString()

		self.send(payload)	

	def createRoom(self,roomId, maxPlayers):
		payload = self.packet.CreateRoomPacket()
		payload.type = self.packet.CREATE_ROOM
		payload.room_id = roomId
		payload.max_players = maxPlayers
		payload.player.name = self.user

		payload = payload.SerializeToString()
		self.send(payload)

		self.join(roomId)
		
	def join(self, roomId):
		payload = self.packet.JoinPacket()
		payload.type = self.packet.JOIN
		payload.room_id = roomId
		payload.player.name = self.user

		payload = payload.SerializeToString()
		self.send(payload)

	def getPlayers(self,roomId):
		payload = self.packet.PlayerListPacket()
		payload.type = self.packet.PLAYER_LIST
		payload.room_id = roomId

		payload = payload.SerializeToString()
		self.send(payload)

'''
	def leave():
		return 0
	

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
		elif message == "join room":
			roomId = input(">roomId: ")
			client.join(roomId)
		elif message == "get players":
			roomId = input(">roomId: ")
			client.getPlayers(roomId)
		elif message == "q":
			self._socket.close()
			break
