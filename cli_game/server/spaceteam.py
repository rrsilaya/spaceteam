

class SpaceTeam:
  def __init__(self, lobby):
    self.lobby = lobby
    self.players = []

    self.state = None
    self.clock = 0

  def getPlayerId(address):
    ip_addr, port = address

    return '{}:{}'.format(ip_addr, port)

  def addPlayer(self, address):
    ip_addr, port = address

    self.players.append({
      'ip_addr': ip_addr,
      'port': port,
      'ready': False
    })

  def removePlayer(self, address):
    ip_addr, port = address
    
    self.players = [*filter(
      lambda player:
        player['ip_addr'] != ip_addr or player['port'] != port,
      self.players
    )]

  def toggleReady(self, address, state):
    ip_addr, port = address

    self.players = [*map(
      lambda player:
          { **player, 'ready': state }
        if player['ip_addr'] == ip_addr and player['port'] == port
        else player,
      self.players
    )]

    # Check if all players are ready
    if all([player['ready'] for player in self.players]):
      return True
    else:
      return False
