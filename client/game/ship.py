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

    self.controls = {
      'HSWITCH1': False,
      'VSWITCH1': False,
    }

    self._loadView()
    self._preparePanels()
    self._prepareControls()
    Thread(target=self.clockTick).start()

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

    # self.addPanel(width=1, height=1, gridPos=(1, 1))
    self.addPanel(width=1, height=1, gridPos=(2, 1))
    self.addPanel(width=3, height=1, gridPos=(1, 2))
    # self.addPanel(width=1, height=1, gridPos=(4, 2))

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

    self.create_text(30, 150, text='▶  Engage Elgenthrottle', fill='white', font=_getFont('heading'), anchor=tk.W)

  def clockTick(self):
    tick = 50

    while tick >= 0:
      c = self.coords('TIMER')
      self.coords('TIMER', c[0], c[1], tick * 14, c[3])

      if c[2] == 420:
        self.itemconfig('TIMER', fill='yellow')
      elif c[2] == 210:
        self.itemconfig('TIMER', fill='red')

      tick -= 1
      sleep(0.1)

  def _prepareControls(self):
    hswitch1 = Switch(self, 'Calcium Razor', 'CALCIUM_RAZOR', (0, 0))
    vswitch1 = Switch(self, 'Arcball Pendulum', 'ARCBALL_PENDULUM', (2, 1), horizontal=False)
    binbtn = BinaryButton(self, 'Salty Cannister', 'SALTY_CANNISTER', (1, 0))
    btngrp = ButtonGroup(self, 'Protolube Optimizer', 'PROTOLUBE_OPTIMIZER', (3, 0), ['Defragment', 'Fragment'])
    vslider = VerticalSlider(self, 'Quasipaddle', 'QUASIPADDLE', (0, 1))
    hslider = HorizontalSlider(self, 'Psylocibin Capacitor', 'PSYLOCIBIN_CAPACITOR', (1, 2))

