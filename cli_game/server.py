from server import UdpServer, SpaceTeam, commands
from proto.spaceteam_pb2 import SpaceteamPacket
from time import sleep
from threading import Thread

class App:
  def __init__(self):
    self.connection = UdpServer()
    self.packet = SpaceteamPacket()

    self.players = {}
    self.games = {}

  def _parse(type, packet):
    data = type()
    data.ParseFromString(packet)

    return data

  def _handleConnect(self, data, address):
    ip_addr, port = address
    data = App._parse(self.packet.ConnectPacket, data)
      
    if not data.lobby_id in self.games:
      self.games[data.lobby_id] = SpaceTeam(data.lobby_id, self)

    # Add to room
    # @TODO: Avoid duplicates and limit with number of players
    self.games[data.lobby_id].addPlayer(address)

    payload = self.packet.GameStatePacket()
    payload.type = self.packet.GAME_STATE
    payload.player_count = len(self.games[data.lobby_id].players)
    payload.update = self.packet.GameStatePacket.CONNECT
    payload.screen = self.packet.GameStatePacket.LOBBY

    self.connection.broadcast(self.games[data.lobby_id].players, payload)

    self.players[SpaceTeam.getPlayerId(address)] = data.lobby_id
    print('[CONNECT] New player connected to lobby!')

  def _handleDisconnect(self, data, address):
    ip_addr, port = address
    data = App._parse(self.packet.ConnectPacket, data)

    player = SpaceTeam.getPlayerId(address)

    if player in self.players:
      lobby_id = self.players[player]

      self.games[lobby_id].removePlayer(address)

      if player in self.players:
        payload = self.packet.GameStatePacket()
        payload.type = self.packet.GAME_STATE
        payload.player_count = len(self.games[lobby_id].players)
        payload.update = self.packet.GameStatePacket.DISCONNECT

        self.connection.broadcast(self.games[lobby_id].players, payload)

        del(self.players[player])
        print('[DISCONNECT] Player has disconnected from the lobby!')

  def _handleReady(self, data, address):
    ip_addr, port = address
    data = App._parse(self.packet.ReadyPacket, data)

    lobby_id = self.players[SpaceTeam.getPlayerId(address)]
    ready = self.games[lobby_id].toggleReady(address, data.toggle)

    payload = self.packet.ReadyPacket()
    payload.type = self.packet.READY
    payload.toggle = data.toggle
    payload.player_id = str(port)

    self.connection.broadcast(self.games[lobby_id].players, payload)
    
    if data.toggle: print('[READY] Player {} is ready!'.format(port))
    else: print('[READY] Player {} is not ready!'.format(port))

    if ready:# and len(self.games[lobby_id].players) > 1:
      
      payload = self.packet.GameStatePacket()
      payload.type = self.packet.GAME_STATE
      payload.sector = 1
      payload.update = self.packet.GameStatePacket.SECTOR

      self.connection.broadcast(self.games[lobby_id].players, payload)

      self.games[lobby_id].start()
      
  def _clockTick(self, lobby, address, time, **kw):
    self.games[lobby].clock = time

    for remaining in range(time, -1, -1):
      self.games[lobby].clock = remaining

      payload = self.packet.GameStatePacket()
      payload.type = self.packet.GAME_STATE
      payload.clock = remaining
      payload.update = self.packet.GameStatePacket.CLOCK_TICK
      if 'screen' in kw: payload.screen = kw['screen']

      if type(address) is list:
        self.connection.broadcast(address, payload)
      else:
        self.connection.send((address['ip_addr'], address['port']), payload)

      sleep(0.1)

    if 'callback' in kw:
      kw['callback']()

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
  app = App()
  app.start()
