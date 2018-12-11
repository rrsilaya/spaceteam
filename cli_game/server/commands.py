import random
from time import sleep
from proto.spaceteam_pb2 import SpaceteamPacket
from threading import Thread

TOGGLE = 0
NUMERIC = 1
CHOICE = 2
SINGLE = 3

class types:
  NO_COMMAND = -1
  CALCIUM_RAZOR = 0
  LORENTZ_WHITTLER = 1
  KILOBYPASS_TRANSFORMER = 2
  IODINE_SHOWER = 3
  CONTRACTING_PROPELLER = 4
  QUASIPADDLE = 5
  HOLOSPINDLE = 6
  ARCBALL_PENDULUM = 7
  PRESSURIZED_VARNISH = 8
  ORBRING = 9
  FLUXLOOSENER_INDUCER = 10
  PROTOLUBE_OPTIMIZER = 11
  PSILOCYBIN_CAPACITOR = 12
  SALTY_CANISTER = 13
  ALTITUDE_OPERATOR = 14

class Command:
  def __init__(self, type, server, **kw):
    if type == types.CALCIUM_RAZOR:
      self._setInit(
        'Calcium Razor',
        [False, True],
        TOGGLE,
        choices=['Toggle On', 'Toggle Off']
      )
    elif type == types.LORENTZ_WHITTLER:
      self._setInit(
        'Lorenz Whittler',
        [ i + 1 for i in range(5) ],
        NUMERIC
      )
    elif type == types.KILOBYPASS_TRANSFORMER:
      self._setInit(
        'Kilobypass Transformer',
        [False, True],
        TOGGLE,
        choices=['Engage', 'Disengage']
      )
    elif type == types.IODINE_SHOWER:
      self._setInit(
        'Iodine Shower',
        ['Infuse', 'Diffuse'],
        CHOICE
      )
    elif type == types.CONTRACTING_PROPELLER:
      self._setInit(
        'Contracting Propeller',
        ['Release', 'Kick', 'Acquire'],
        CHOICE
      )
    elif type == types.QUASIPADDLE:
      self._setInit(
        'Quasipaddle',
        [ i + 1 for i in range(5) ],
        NUMERIC
      )
    elif type == types.HOLOSPINDLE:
      self._setInit(
        'Holospindle',
        [ i + 1 for i in range(2) ],
        CHOICE
      )
    elif type == types.ARCBALL_PENDULUM:
      self._setInit(
        'Arcball Pendulum',
        [False, True],
        TOGGLE,
        choices=['Turn On', 'Turn Off']
      )
    elif type == types.PRESSURIZED_VARNISH:
      self._setInit(
        'Pressurized Varnish',
        [ i + 1 for i in range(3) ],
        NUMERIC
      )
    elif type == types.ORBRING:
      self._setInit(
        'Orbring',
        ['Power Up', 'Power Down'],
        CHOICE
      )
    elif type == types.FLUXLOOSENER_INDUCER:
      self._setInit(
        'Fluxloosener Inducer',
        ['Flush'],
        CHOICE
      )
    elif type == types.PROTOLUBE_OPTIMIZER:
      self._setInit(
        'Protolube Optimizer',
        [False, True],
        TOGGLE,
        choices=['Fragment', 'Defragment']
      )
    elif type == types.PSILOCYBIN_CAPACITOR:
      self._setInit(
        'Psilocybin Capacitor',
        [ (i * 10) + 50 for i in range(5) ],
        NUMERIC
      )
    elif type == types.SALTY_CANISTER:
      self._setInit(
        'Salty Canister',
        [False, True],
        TOGGLE,
        choices=['Open', 'Close']
      )
    elif type == types.ALTITUDE_OPERATOR:
      self._setInit(
        'Altitude Operator',
        ['Approach', 'Kick'],
        CHOICE
      )
    elif type == types.NO_COMMAND:
      self._setInit(
        'No Command',
        [types.NO_COMMAND],
        types.NO_COMMAND
      )


    self.server = server
    self.packet = SpaceteamPacket()
    self.state = self.states[0]
    self.time = 0
    self.isResolved = True
    self.callbacks = kw

  def _setInit(self, name, states, type, **kw):
    self.name = name
    self.states = states
    self.type = type
    self.choices = kw['choices'] if 'choices' in kw else None

  def changeState(self, state):
    if state in self.states:
      self.state = state

  def getRandomCommand(self):
    command = random.randrange(len(self.states))

    while self.type != CHOICE and command == self.state:
      command = random.randrange(len(self.states))

    self.command = self.choices[command] if self.choices else self.states[command]
    return str(command)

  def tick(self, address):
    payload = self.packet.GameStatePacket()
    payload.type = self.packet.GAME_STATE
    payload.clock = self.time
    payload.total_time = self.time
    payload.update = self.packet.GameStatePacket.CLOCK_TICK
    payload.screen = self.packet.GameStatePacket.SHIP

    self.server.connection.send(address, payload)
    while self.time > 0 and not self.isResolved:
      self.time -= 1
      payload.clock = self.time

      self.server.connection.send(address, payload)
      sleep(0.1)

    if not self.isResolved and self.command != str(types.NO_COMMAND):
      print('Failed to execute command <{}: {}>'.format(self.name, self.command))
      self.callbacks['updateLife'](-25)
      self.isResolved = True

  def spawn(self, address):
    self.isResolved = False
<<<<<<< HEAD
    self.time = 120

=======
    self.time = 50
>>>>>>> c7e2817ff07502456d3d6f48d7ae7fc17c7e91ca
    if (self.type != types.NO_COMMAND):
      self.command = self.getRandomCommand()
    else:
      self.command = str(types.NO_COMMAND)

    payload = self.packet.CommandPacket()
    payload.type = self.packet.COMMAND
    payload.panel = self.name
    payload.command = self.command

    print('> {}: {}'.format(self.name, payload.command))

    self.server.connection.send(address, payload)
    if (self.type != types.NO_COMMAND):
      Thread(target=self.tick, args=[address]).start()
    else:
      self.tick(address)
