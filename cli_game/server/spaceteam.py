import random
from server import Command, commands

from proto.spaceteam_pb2 import SpaceteamPacket


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

    self.packet = SpaceteamPacket()

    self.collection_commands = [
      commands.types.CALCIUM_RAZOR,
      commands.types.LORENTZ_WHITTLER,
      commands.types.KILOBYPASS_TRANSFORMER,
      commands.types.IODINE_SHOWER,
      commands.types.CONTRACTING_PROPELLER,
      commands.types.QUASIPADDLE,
      commands.types.HOLOSPINDLE,
      commands.types.ARCBALL_PENDULUM,
      commands.types.PRESSURIZED_VARNISH,
      commands.types.ORBRING,
      commands.types.FLUXLOOSENER_INDUCER,
      commands.types.PROTOLUBE_OPTIMIZER,
      commands.types.PSILOCYBIN_CAPACITOR,
      commands.types.SALTY_CANISTER,
      commands.types.ALTITUDE_OPERATOR,
      commands.types.WAVEFORM_COLLIDER,
      commands.types.ALPHA_WAVE,
      commands.types.GLYCOL_PUMP,
      commands.types.CABIN_FAN,
      commands.types.GAMMA_RADIATOR,
      commands.types.THERMONUCLEAR_RESONATOR,
      commands.types.DOCKING_PROBE,
      commands.types.SCE_POWER,
      commands.types.SUIT_COMPOSITION,
      commands.types.H2O_FLOW,
      commands.types.WASTE_DUMP,
      commands.types.INT_LIGHTS
    ]

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
      if(self.commands[cmd].command.upper() == command.upper()) and (self.commands[cmd].name.upper() == panel.upper()):
        self.commands[cmd].isResolved = True
        self.updateLife(25)
        print("Successfully Resolved", panel, " to ", command)
        break


  def start(self):
    no_command = Command(commands.types.NO_COMMAND,self.server)
    no_command.spawn(self.players)

    panels = self.collection_commands
    print(panels)
    return 0
    
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
      print("End Game")
