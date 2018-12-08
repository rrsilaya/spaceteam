TOGGLE = 0
NUMERIC = 1
CHOICE = 2

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
        [False, True],
        TOGGLE,
        choices=['Infuse', 'Diffuse']
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

