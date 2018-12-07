from server import UdpServer
from proto.spaceteam_pb2 import SpaceteamPacket

class SpaceTeam:
  def __init__(self):
    self.connection = UdpServer()
    self.packet = SpaceteamPacket()

    self.rooms = {}
    self.players = {}

  def _parse(type, packet):
    data = type()
    data.ParseFromString(packet)

    return data

  def _handleConnect(self, data, address):
    ip_addr, port = address
    data = SpaceTeam._parse(self.packet.ConnectPacket, data)
      
    if not data.lobby_id in self.rooms:
      self.rooms[data.lobby_id] = []

    # Add to room
    # @TODO: Avoid duplicates and limit with number of players
    self.rooms[data.lobby_id].append({
      'ip_addr': ip_addr,
      'port': port,
      'ready': False
    })

    payload = self.packet.GameStatePacket()
    payload.type = self.packet.GAME_STATE
    payload.player_count = len(self.rooms[data.lobby_id])
    payload.update = self.packet.GameStatePacket.CONNECT

    self.connection.broadcast(self.rooms[data.lobby_id], payload)

    self.players['{}:{}'.format(ip_addr, port)] = data.lobby_id
    print('[CONNECT] New player connected to lobby!')

  def _handleDisconnect(self, data, address):
    ip_addr, port = address
    data = SpaceTeam._parse(self.packet.ConnectPacket, data)

    lobby_id = self.players['{}:{}'.format(ip_addr, port)]

    self.rooms[lobby_id] = [*filter(
      lambda player:
        player['ip_addr'] != ip_addr or player['port'] != port,
      self.rooms[lobby_id]
    )]

    player = '{}:{}'.format(ip_addr, port)
    if player in self.players:
      payload = self.packet.GameStatePacket()
      payload.type = self.packet.GAME_STATE
      payload.player_count = len(self.rooms[lobby_id])
      payload.update = self.packet.GameStatePacket.DISCONNECT

      self.connection.broadcast(self.rooms[lobby_id], payload)

      del(self.players[player])
      print('[DISCONNECT] Player has disconnected from the lobby!')

  def _handleReady(self, data, address):
    ip_addr, port = address
    data = SpaceTeam._parse(self.packet.ReadyPacket, data)

    lobby_id = self.players['{}:{}'.format(ip_addr, port)]

    self.rooms[lobby_id] = [*map(
      lambda player:
          { **player, 'ready': data.toggle }
        if player['ip_addr'] == ip_addr and player['port'] == port
        else player,
      self.rooms[lobby_id]
    )]

    payload = self.packet.ReadyPacket()
    payload.type = self.packet.READY
    payload.toggle = data.toggle
    payload.player_id = str(port)

    self.connection.broadcast(self.rooms[lobby_id], payload)
    
    if data.toggle: print('[READY] Player {} is ready!'.format(port))
    else: print('[READY] Player {} is not ready!'.format(port))

  def parsePacket(self, data, address):
    self.packet.ParseFromString(data)

    if self.packet.type == self.packet.CONNECT:
      self._handleConnect(data, address)
    elif self.packet.type == self.packet.DISCONNECT:
      self._handleDisconnect(data, address)
    elif self.packet.type == self.packet.READY:
      self._handleReady(data, address)

  def start(self):
    self.connection.listen(self.parsePacket)

if __name__ == '__main__':
  app = SpaceTeam()
  app.start()
