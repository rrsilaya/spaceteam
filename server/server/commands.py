import random
from time import sleep
from proto.spaceteam_pb2 import SpaceteamPacket
from threading import Thread

TOGGLE = 0
NUMERIC = 1
CHOICE = 2
BINARY = 3
NO_COMMAND = 4

class types:
  NO_COMMAND = "NO_COMMAND"

  CALCIUM_RAZOR = 0
  SALTY_CANNISTER = 1
  WAVEFORM_COLLIDER = 2
  PROTOLUBE_OPTIMIZER = 3
  QUASIPADDLE = 4
  PSYLOCIBIN_CAPACITOR = 5
  ARCBALL_PENDULUM = 6

  LORENTZ_WHITTLER = 7
  ALPHA_WAVE = 8
  HOLOSPINDLE = 9
  CONTRACTING_PROPELLER = 10
  IODINE_SHOWER = 11
  ORBRING = 12

  KILOBYPASS_TRANSFORMER = 13
  ALTITUDE_OPERATOR = 14
  GLYCOL_PUMP = 15
  FLUXLOOSENER_INDUCER = 16
  PRESSURIZED_VARNISH = 17
  CABIN_FAN = 18
  GAMMA_RADIATOR = 19

  THERMONUCLEAR_RESONATOR = 20
  DOCKING_PROBE = 21
  SCE_POWER = 22
  SUIT_COMPOSITION = 23
  H2O_FLOW = 24
  WASTE_DUMP = 25
  INT_LIGHTS = 26

class Command:
  def __init__(self, type, server, **kw):
    if type == types.CALCIUM_RAZOR:
      self._setInit('Calcium Razor', TOGGLE)
    elif type == types.SALTY_CANNISTER:
      self._setInit('Salty Cannister', BINARY)
    elif type == types.WAVEFORM_COLLIDER:
      self._setInit('Waveform Collider', BINARY)
    elif type == types.PROTOLUBE_OPTIMIZER:
      self._setInit('Protolube Optimizer', CHOICE, states=['Defragment', 'Fragment'])
    elif type == types.QUASIPADDLE:
      self._setInit('Quasipaddle', NUMERIC, range=3)
    elif type == types.PSYLOCIBIN_CAPACITOR:
      self._setInit('Psylocibin Capacitor', NUMERIC, range=5)
    elif type == types.ARCBALL_PENDULUM:
      self._setInit('Arcball Pendulum', TOGGLE)
    elif type == types.LORENTZ_WHITTLER:
      self._setInit('Lorentz Whittler', NUMERIC, range=3)
    elif type == types.ALPHA_WAVE:
      self._setInit('Alpha Wave', NUMERIC, range=3)
    elif type == types.HOLOSPINDLE:
      self._setInit('Holospindle', BINARY)
    elif type == types.CONTRACTING_PROPELLER:
      self._setInit('Contracting Propeller', CHOICE, states=['Acquire', 'Kick'])
    elif type == types.IODINE_SHOWER:
      self._setInit('Iodine Shower', NUMERIC, range=5)
    elif type == types.ORBRING:
      self._setInit('Orbring', TOGGLE)
    elif type == types.KILOBYPASS_TRANSFORMER:
      self._setInit('Kilobypass Transformer', CHOICE, states=['Engage', 'Disengage'])
    elif type == types.ALTITUDE_OPERATOR:
      self._setInit('Altitude Operator', TOGGLE)
    elif type == types.GLYCOL_PUMP:
      self._setInit('Glycol Pump', TOGGLE)
    elif type == types.FLUXLOOSENER_INDUCER:
      self._setInit('Fluxloosener Inducer', NUMERIC, range=5)
    elif type == types.PRESSURIZED_VARNISH:
      self._setInit('Pressurized Varnish', NUMERIC, range=3)
    elif type == types.CABIN_FAN:
      self._setInit('Cabin Fan', BINARY)
    elif type == types.GAMMA_RADIATOR:
      self._setInit('Gamma Radiator', TOGGLE)
    elif type == types.THERMONUCLEAR_RESONATOR:
      self._setInit('Thermonuclear Resonator', NUMERIC, range=5)
    elif type == types.DOCKING_PROBE:
      self._setInit('Docking Probe', CHOICE, states=['Extend', 'Retract'])
    elif type == types.SCE_POWER:
      self._setInit('SCE Power', NUMERIC, range=3)
    elif type == types.SUIT_COMPOSITION:
      self._setInit('Suit Composition', BINARY)
    elif type == types.H2O_FLOW:
      self._setInit('H2O Flow', TOGGLE)
    elif type == types.WASTE_DUMP:
      self._setInit('Waste Dump', TOGGLE)
    elif type == types.INT_LIGHTS:
      self._setInit('Int Lights', NUMERIC, range=3)
    elif type == types.NO_COMMAND:
      self._setInit(types.NO_COMMAND, NO_COMMAND)

    self.server = server
    self.packet = SpaceteamPacket()
    self.state = self.states[0]
    self.time = 0
    self.isResolved = True
    self.callbacks = kw

  def _setInit(self, name, type, **kw):
    self.name = name
    self.type = type

    if type == TOGGLE:
      self.states = ['False', 'True']
    elif type == NUMERIC:
      self.states = [str(i) for i in range(kw['range'])]
    elif type == BINARY:
      self.states = [0, 1]
    elif type == CHOICE:
      self.states = kw['states']
    elif type == NO_COMMAND:
      self.states = [types.NO_COMMAND]

  def changeState(self, state):
    if state in self.states:
      self.state = state

  def getRandomCommand(self):
    command = random.randrange(len(self.states))

    while (self.type == TOGGLE or self.type == NUMERIC) and self.states[command] == self.state:
      command = random.randrange(len(self.states))

    self.command = self.states[command]
    return str(self.command)

  def tick(self, address):
    payload = self.packet.GameStatePacket()
    payload.type = self.packet.GAME_STATE
    payload.clock = self.time
    payload.total_time = self.time
    payload.update = self.packet.GameStatePacket.CLOCK_TICK
    payload.screen = self.packet.GameStatePacket.SHIP

    if self.command != types.NO_COMMAND:
      self.server.connection.send(address, payload)
    else:
      self.server.connection.broadcast(address, payload)
    while self.time > 0 and not self.isResolved:
      self.time -= 1
      payload.clock = self.time

      if self.command != types.NO_COMMAND:
        self.server.connection.send(address, payload)
      else:
        self.server.connection.broadcast(address, payload)
      sleep(0.1)

    if not self.isResolved and self.command != types.NO_COMMAND:
      print('Failed to execute command <{}: {}>'.format(self.name, self.command))
      self.callbacks['updateLife'](-25)
      self.isResolved = True

  def spawn(self, address):
    self.isResolved = False
    self.time = 40

    if (self.type != NO_COMMAND):
      self.command = self.getRandomCommand()
    else:
      self.command = types.NO_COMMAND

    payload = self.packet.CommandPacket()
    payload.type = self.packet.COMMAND
    payload.panel = self.name
    payload.command = self.command

    print('> {}: {}'.format(self.name, payload.command))

    if (self.type != NO_COMMAND):
      self.server.connection.send(address, payload)
      Thread(target=self.tick, args=[address]).start()
    else:
      self.server.connection.broadcast(address, payload)
      self.tick(address)
