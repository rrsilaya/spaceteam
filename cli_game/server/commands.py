TOGGLE = 0
NUMERIC = 1
CHOICE = 2
SINGLE = 3

class types:
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
  def __init__(self, type):
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

    self.state = states[0]

  def _setInit(self, name, states, type, **kw):
    self.name = name
    self.states = states
    self.type = type
    
    if 'choices' in kw:
      self.choices = choices

  def changeState(self, state):
    if state in self.states:
      self.state = state

