import random
from server import Command

BASE_COMMAND_COUNT = 10
BASE_TIME = 50

class SpaceTeam:
  def __init__(self, lobby, server):
    self.lobby = lobby
    self.server = server

    self.players = []
    self.commands = []

    self.state = None
    self.clock = 0
    self.sector = 1
    self.givenCommands = BASE_COMMAND_COUNT
    self.life = 100

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

  def updateLife(self, amount):
    self.life += amount
    
    # if self.life > 100:
    #   self.life = 100
    print('[LIFE] Life Remaining: {}'.format(self.life))


  def checkResolved(self, panel, command):
    for cmd in range(len(self.commands)):
      if(self.commands[cmd].command == command) and (self.commands[cmd].name == panel):
        self.commands[cmd].isResolved = True
        self.updateLife(25)
        print("Successfully Resolved", panel, " to ", command)
        break


  def start(self):
    panels = random.sample([ i for i in range(15) ], self.givenCommands)
    panels = [ Command(panel, self.server, updateLife=self.updateLife) for panel in panels ]

    self.commands = random.sample(panels, len(self.players))

    while self.life > 0:      
      for cmd in range(len(self.commands)):
        if self.commands[cmd].isResolved:
          # Populate with new commands
          address = (self.players[cmd]['ip_addr'], self.players[cmd]['port'])
          self.commands[cmd] = random.sample(panels, 1)[0]
          self.commands[cmd].spawn(address)
    if(self.life) == 0:
      for cmd in range(len(self.commands)):
          self.commands[cmd].isResolved = True
          print("Resolved GAME OVER")
      self.server.GameOver(self.lobby)