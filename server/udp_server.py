from socket import AF_INET, socket, SOCK_DGRAM

#di ako sure kung tama to
import sys
sys.path.append('./../client')
from proto.udp_packet_pb2 import UdpPacket

HOST = 'localhost'
TCP_PORT = 80
UDP_PORT = 3003
BUFFER = 4096

class UDPServer():
	rooms = {}
	def __init__(self):
		self.address = (HOST, UDP_PORT)
		self._socket = socket(AF_INET, SOCK_DGRAM)
		self._socket.connect(self.address)
		self.packet = UdpPacket()

	def run(self):
		self._socket = socket(AF_INET, SOCK_DGRAM)
		self._socket.bind(self.address)
		print("Started Server")


		while True:
			data, addr = self._socket.recvfrom(BUFFER)
			self.packet.ParseFromString(data)
			print(self.packet.type)
			if self.packet.type == self.packet.CONNECT:
				packet = self.packet.ConnectPacket()
				packet.ParseFromString(data)

				print(packet.player.name + " connected to the server")


			elif self.packet.type == self.packet.CREATE_ROOM:
				print(self.rooms)
				packet = self.packet.CreateRoomPacket()
				packet.ParseFromString(data)
				print(packet)
				roomId=packet.room_id
				self.rooms[roomId] = packet
				print (packet.player.name + ' has created a room')
				print(self.rooms)

			'''
			elif data.PacketType == 'LEAVE':
			elif data.PacketType == 'JOIN':
			elif data.PacketType == 'PLAY':
				print("Not yet implemented")
			elif data.PacketType == 'PLAYER_LIST':
			elif data.PacketType == 'ERR_RDNE':
				print("Room does not exist")
			elif data.PacketType == 'ERR_RFULL':
				print("Room full")
			else:
				print("Packet error")
			'''
			
			
			

	
	
	


	def stop(self):
		self._socket.close()

if __name__ == "__main__":
	server = UDPServer()
	server.run()