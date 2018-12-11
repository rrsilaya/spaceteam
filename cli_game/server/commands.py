import random
from time import sleep
from proto.spaceteam_pb2 import SpaceteamPacket
from threading import Thread

TOGGLE = 0
NUMERIC = 1
CHOICE = 2
SINGLE = 3

class types:
  NO_COMMAND = "NO_COMMAND"
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
  WAVEFORM_COLLIDER = 15
  ALPHA_WAVE = 16
  GLYCOL_PUMP = 17
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
      self._setInit(
        'Calcium Razor',
        [False, True],
        TOGGLE
      )
    elif type == types.LORENTZ_WHITTLER:
      self._setInit(
        'Lorenz Whittler',
        [i for i in range(3)],
        NUMERIC
      )
    elif type == types.KILOBYPASS_TRANSFORMER:
      self._setInit(
        'Kilobypass Transformer',
        ['Engage', 'Disengage']
        CHOICE
      )
    elif type == types.IODINE_SHOWER:
      self._setInit(
        'Iodine Shower',
        [i + 1 for i in range(3)],
        NUMBERICS
      )
    elif type == types.CONTRACTING_PROPELLER:
      self._setInit(
        'Contracting Propeller',
        ['Acquire','Kick'],
        CHOICE
      )
    elif type == types.QUASIPADDLE:
      self._setInit(
        'Quasipaddle',
        [i + 1 for i in range(3)],
        NUMERIC
      )
    elif type == types.HOLOSPINDLE:
      self._setInit(
        'Holospindle',
        [0,1],
        CHOICE
      )
    elif type == types.ARCBALL_PENDULUM:
      self._setInit(
        'Arcball Pendulum',
        [False,True],
        TOGGLE
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
        [False,True],
        TOGGLE
      )
    elif type == types.FLUXLOOSENER_INDUCER:
      self._setInit(
        'Fluxloosener Inducer',
        [ i for i in range(3) ],
        CHOICE
      )
    elif type == types.PROTOLUBE_OPTIMIZER:
      self._setInit(
        'Protolube Optimizer',
        ['Defragment','Fragment'],
        CHOICE
      )
    elif type == types.PSILOCYBIN_CAPACITOR:
      self._setInit(
        'Psilocybin Capacitor',
        [ i for i in range(5) ],
        NUMERIC
      )
    elif type == types.SALTY_CANISTER:
      self._setInit(
        'Salty Canister',
        [0,1],
        CHOICE
      )
    elif type == types.ALTITUDE_OPERATOR:
      self._setInit(
        'Altitude Operator',
        [False, True],
        TOGGLE
      )
    elif type == types.WAVEFORM_COLLIDER:
      self._setInit(
        'Waveform Collider',
        [0,1],
        CHOICE
      )   
    elif type == types.ALPHA_WAVE:
      self._setInit(
        'Alpha Wave',
        [i for i in range(3)],
        NUMERIC
      )     
    elif type == types.GLYCOL_PUMP:
       self._setInit(
        'Glycol Pump',
        [False,True],
        TOGGLE
      )       
    elif type == types.CABIN_FAN:
      self._setInit(
        'Cabin Fan',
        [0,1],
        CHOICE
      )
    elif type == types.GAMMA_RADIATOR:
      self._setInit(
        'Gamma Radiator',
        [False,True],
        TOGGLE
      )
    elif type == types.THERMONUCLEAR_RESONATOR:
      self._setInit(
        'Thermonuclear Resonator',
        [ i for i in range(5) ],
        NUMERIC
      )    
    elif type == types.DOCKING_PROBE:
      self._setInit(
        'Docking Probe',
        ['Extend', 'Retract'],
        CHOICE
      ) 
    elif type == types.SCE_POWER:
      self._setInit(
        'SCE Power',
        [ i for i in range(3) ],
        NUMERIC
      ) 
    elif type == types.SUIT_COMPOSITION:
      self._setInit(
        'Suit Composition',
        [ 0,1 ],
        CHOICE
      ) 
    elif type == types.H2O_FLOW:
      self._setInit(
        'H2O Flow',
        [ False,True ],
        TOGGLE
      ) 
    elif type == types.WASTE_DUMP:
      self._setInit(
        'Waste Dump',
        [ False,True ],
        TOGGLE
      )
    elif type == types.INT_LIGHTS:
      self._setInit(
        'Int Lights',
        [  i for i in range(3) ],
        NUMERIC
      )
    elif type == types.NO_COMMAND:
      self._setInit(
        types.NO_COMMAND,
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

    if (self.type != types.NO_COMMAND):
      self.command = self.getRandomCommand()
    else:
      self.command = types.NO_COMMAND

    payload = self.packet.CommandPacket()
    payload.type = self.packet.COMMAND
    payload.panel = self.name
    payload.command = self.command

    print('> {}: {}'.format(self.name, payload.command))

    if (self.type != types.NO_COMMAND):
      self.server.connection.send(address, payload)
      Thread(target=self.tick, args=[address]).start()
    else:
      self.server.connection.broadcast(address, payload)
      self.tick(address)
