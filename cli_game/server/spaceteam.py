import random
from server import Command, commands

from proto.spaceteam_pb2 import SpaceteamPacket
from threading import Thread

BASE_TIME = 50

LOSE_POINTS = 0
WIN_POINTS = 200
POINT_INCREMENT = 15
POINT_DECREMENT = 15

class SpaceTeam:
  def __init__(self, lobby, server):
    self.lobby = lobby
    self.server = server

    self.players = []
    self.commands = []

    self.state = None
    self.clock = 0
    self.sector = 1
    self.life = 100

    self.packet = SpaceteamPacket()

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
      slug = self.commands[cmd].name.upper().replace(' ', '_')
      props = str(self.commands[cmd].command).upper()

      print(slug, props, command, panel)
      if(slug == command) and (props == str(panel).upper()):
        self.commands[cmd].isResolved = True
        self.commands[cmd].state = self.commands[cmd].command
        self.updateLife(25)
        print("Successfully Resolved", panel, " to ", command)
        break

  def _start(self):
    no_command = Command(commands.types.NO_COMMAND, self.server)
    no_command.spawn(self.players)

    if len(self.players) == 1: panelRange = 7
    elif len(self.players) == 2: panelRange = 13
    elif len(self.players) == 3: panelRange = 20
    elif len(self.players) == 4: panelRange = 27
    else: return

    panels = [ i for i in range(panelRange) ]
    panels = [ Command(panel, self.server, updateLife=self.updateLife) for panel in panels ]

    print([i.name for i in panels])

    self.commands = random.sample(panels, len(self.players))

    while self.life > LOSE_POINTS and self.life < WIN_POINTS:
      for cmd in range(len(self.commands)):
        if self.commands[cmd].isResolved:
          # Populate with new commands
          address = (self.players[cmd]['ip_addr'], self.players[cmd]['port'])
          self.commands[cmd] = random.sample(panels, 1)[0]
          self.commands[cmd].spawn(address)

    packet = self.packet
    payload = packet.GameStatePacket()
    payload.type = packet.GAME_STATE
    payload.update = packet.GameStatePacket.GAME_OVER

    
    for cmd in range(len(self.commands)):
      self.commands[cmd].isResolved = True
      
    if self.life <= LOSE_POINTS:
      payload.isWin = False
      self.server.connection.broadcast(self.players, payload)
    elif self.life >= WIN_POINTS:
      payload.isWin = True
      self.server.connection.broadcast(self.players, payload)

  def start(self):
    Thread(target=self._start).start()