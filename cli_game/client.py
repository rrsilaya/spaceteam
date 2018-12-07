from socket import AF_INET, socket, SOCK_DGRAM
from proto.spaceteam_pb2 import SpaceteamPacket
from re import match
from threading import Thread

HOST = 'localhost'
TCP_PORT = 80
UDP_PORT = 3003
BUFFER = 4096

class UdpConnection:
  def __init__(self):
    self.address = (HOST, UDP_PORT)

    self._socket = socket(AF_INET, SOCK_DGRAM)
    self.active = True

  def send(self, data):
    self._socket.sendto(data.SerializeToString(), self.address)

  def _receive(self):
    while self.active:
      try:
        data, address = self._socket.recvfrom(BUFFER)

        self.recvCallback(data)
      except Exception as e:
        print('An error occured')
        print(e)
        break

  def listen(self, recvCallback):
    self.recvCallback = recvCallback
    Thread(target=self._receive).start()

if __name__ == '__main__':
  app = UdpConnection()
  packet = SpaceteamPacket()

  def _parse(type, packet):
    data = type()
    data.ParseFromString(packet)

    return data

  def parser(data):
    packet.ParseFromString(data)

    if packet.type == packet.GAME_STATE:
      data = _parse(packet.GameStatePacket, data)

      if data.update == 0:
        print('New player has connected. PLAYERS: %i' % data.player_count)
      elif data.update == 1:
        print('A player has  disconnected. PLAYERS: %i' % data.player_count)
    elif packet.type == packet.READY:
      data = _parse(packet.ReadyPacket, data)
      
      if data.toggle: print('Player {} is ready!'.format(data.player_id))
      else: print('Player {} is not ready!'.format(data.player_id))

  app.listen(parser)

  while True:
    message = input('>> ')

    parsed = match(r'(\S+)\s?(\S+)?', message)
    cmd = parsed[1]
    args = parsed[2]
    
    if cmd == 'connect':
      payload = packet.ConnectPacket()
      payload.type = packet.CONNECT

      if args:
        payload.lobby_id = args

      app.send(payload)
    elif cmd == 'disconnect':
      payload = packet.DisconnectPacket()
      payload.type = packet.DISCONNECT

      app.send(payload)
    elif cmd == 'ready':
      payload = packet.ReadyPacket()
      payload.type = packet.READY

      if args == 'false':
        payload.toggle = False
      else:
        payload.toggle = True

      app.send(payload)
