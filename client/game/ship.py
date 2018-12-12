import tkinter as tk
from utils.fonts import _getFont

from game.panel import Switch, BinaryButton, ButtonGroup, VerticalSlider, HorizontalSlider

from time import sleep
from threading import Thread

Y_OFFSET = 220
PANEL_HEIGHT = 127
PANEL_WIDTH = 140

class Ship(tk.Canvas):
  def __init__(self, root):
    tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg='black')
    self.root = root

    self.gameConnection = self.root.gameConnection
    self.udpPacket = self.root.udpPacket

    self._loadView()
    self._preparePanels()
    self._prepareControls(self.root.gameData['player_index'])
    Thread(target=self.clockTick).start()
    Thread(target=self.commandListener).start()

  def addPanel(self, **kw):
    # x: (0:4)
    # y: (0:2)
    width, height, gridPos = (kw['width'], kw['height'], kw['gridPos'])

    self.create_image(
      gridPos[0] * PANEL_WIDTH,
      gridPos[1] * PANEL_HEIGHT + Y_OFFSET,
      image=self.panels['%dx%d' % (width, height)],
      anchor=tk.NW
    )

  def _preparePanels(self):
    circuits = tk.PhotoImage(file='assets/background/circuits.png')
    # Panels
    panel1x1 = tk.PhotoImage(file='assets/panels/1x1.png')
    panel1x2 = tk.PhotoImage(file='assets/panels/1x2.png')
    panel2x1 = tk.PhotoImage(file='assets/panels/2x1.png')
    panel2x2 = tk.PhotoImage(file='assets/panels/2x2.png')
    panel3x1 = tk.PhotoImage(file='assets/panels/3x1.png')

    self.panels = {
      '1x1': panel1x1,
      '1x2': panel1x2,
      '2x1': panel2x1,
      '2x2': panel2x2,
      '3x1': panel3x1
    }
    self.circuits = circuits.zoom(2)
    self.create_image(700, Y_OFFSET, image=self.circuits, anchor=tk.NE)

  def _loadView(self):
    ship = tk.PhotoImage(file='assets/elements/ship-small.png')
    instruction = tk.PhotoImage(file='assets/elements/instruction.png')
    timer_empty = tk.PhotoImage(file='assets/elements/timer-empty-transparent.png')
    space = tk.PhotoImage(file='assets/elements/space-top.png')

  def _loadView(self):
    ship = tk.PhotoImage(file='assets/elements/ship-small.png')
    instruction = tk.PhotoImage(file='assets/elements/instruction.png')
    timer_empty = tk.PhotoImage(file='assets/elements/timer-empty-transparent.png')
    space = tk.PhotoImage(file='assets/elements/space-top.png')

    self.ship = ship
    self.instruction = instruction.zoom(3).subsample(2)
    self.timer_empty = timer_empty.zoom(3).subsample(2)
    self.space = space

    self.create_image(0, 0, image=self.space, anchor=tk.NW)
    self.create_image(400, 50, image=self.ship, tags='SHIP')

    # Instruction
    for distance in range(8):
      self.create_image(distance * 95, 100, image=self.instruction, anchor=tk.NW)

    self.create_rectangle(0, 195, 700, 220, fill='green', outline='', tags='TIMER')
    self.create_image(0, 195, image=self.timer_empty, anchor=tk.NW)
    self.create_image(480, 195, image=self.timer_empty, anchor=tk.NW)

    self.create_text(30, 150, text='▶  ' + self.root.gameData['command'], fill='white', font=_getFont('heading'), anchor=tk.W, tags='COMMAND_VIEW')

  def clockTick(self):
    while True:
      tick = self.root.gameData['currentTime']
      total = self.root.gameData['totalTime']

      c = self.coords('TIMER')
      self.coords('TIMER', c[0], c[1], round((tick / total) * 700), c[3])

      if c[2] < 420 and c[2] > 210:
        self.itemconfig('TIMER', fill='yellow')
      elif c[2] < 210:
        self.itemconfig('TIMER', fill='red')

      sleep(0.1)
    
    self.itemconfig('TIMER', fill='green')

  def commandListener(self):
    prevCommand = self.root.gameData['command']

    while True:
      if prevCommand != self.root.gameData['command']:
        prevCommand = self.root.gameData['command']
        self.itemconfig('COMMAND_VIEW', text='▶  ' + prevCommand)

  def _prepareControls(self, player):
    if player == 0:
      self.controls = [
        Switch(self, 'Calcium Razor', 'CALCIUM_RAZOR', (0, 0)),
        BinaryButton(self, 'Salty Cannister', 'SALTY_CANNISTER', (1, 0)),
        BinaryButton(self, 'Waveform Collider', 'WAVEFORM_COLLIDER', (1, 1)),
        ButtonGroup(self, 'Protolube Optimizer', 'PROTOLUBE_OPTIMIZER', (3, 0), ['Defragment', 'Fragment']),
        VerticalSlider(self, 'Quasipaddle', 'QUASIPADDLE', (0, 1)),
        HorizontalSlider(self, 'Psylocibin Capacitor', 'PSYLOCIBIN_CAPACITOR', (1, 2)),
        Switch(self, 'Arcball Pendulum', 'ARCBALL_PENDULUM', (4, 2), horizontal=False),
      ]
    elif player == 1:
      self.controls = [
        VerticalSlider(self, 'Lorentz Whittler', 'LORENTZ_WHITTLER', (0, 0)),
        VerticalSlider(self, 'Alpha Wave', 'ALPHA_WAVE', (1, 0)),
        BinaryButton(self, 'Holospindle ', 'HOLOSPINDLE', (0, 2)),
        ButtonGroup(self, 'Contracting Propeller', 'CONTRACTING_PROPELLER', (2, 0), ['Acquire', 'Kick']),
        HorizontalSlider(self, 'Iodine Shower', 'IODINE_SHOWER', (2, 2)),
        Switch(self, 'Orbring', 'ORBRING', (4, 0)),
      ]

      self.addPanel(width=1, height=1, gridPos=(4, 1))
    elif player == 2:
      self.controls = [
        ButtonGroup(self, 'Kilobypass Transformer', 'KILOBYPASS_TRANSFORMER', (0, 0), ['Engage', 'Disengage']),
        Switch(self, 'Altitude Operator', 'ALTITUDE_OPERATOR', (0, 2), horizontal=False),
        Switch(self, 'Glycol Pump', 'GLYCOL_PUMP', (1, 2), horizontal=False),
        HorizontalSlider(self, 'Fluxloosener Inducer', 'FLUXLOOSENER_INDUCER', (2, 0)),
        VerticalSlider(self, 'Pressurized Varnish', 'PRESSURIZED_VARNISH', (2, 1)),
        BinaryButton(self, 'Cabin Fan ', 'CABIN_FAN', (3, 2)),
        Switch(self, 'Gamma Radiator', 'GAMMA_RADIATOR', (4, 1)),
      ]

      self.addPanel(width=1, height=1, gridPos=(3, 1))
    elif player == 3:
      self.controls = [
        HorizontalSlider(self, 'Thermonuclear Resonator', 'THERMONUCLEAR_RESONATOR', (0, 0)),
        ButtonGroup(self, 'Docking Probe', 'DOCKING_PROBE', (0, 1), ['Extend', 'Retract']),
        VerticalSlider(self, 'SCE Power', 'SCE_POWER', (2, 1)),
        BinaryButton(self, 'Suit Composition', 'SUIT_COMPOSITION', (3, 0)),
        Switch(self, 'H2O Flow', 'H2O_FLOW', (3, 1)),
        Switch(self, 'Waste Dump', 'WASTE_DUMP', (3, 2)),
        VerticalSlider(self, 'Int Lights', 'INT_LIGHTS', (4, 1)),
      ]
