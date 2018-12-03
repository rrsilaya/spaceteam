import tkinter as tk
from utils.fonts import _getFont

Y_OFFSET = 220
PANEL_HEIGHT = 127
PANEL_WIDTH = 140

class Ship(tk.Canvas):
  def __init__(self, root):
    tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg='black')
    self.root = root

    self._loadView()
    self._preparePanels()

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
    self.addPanel(width=2, height=2, gridPos=(3, 0))
    self.addPanel(width=1, height=1, gridPos=(0, 0))
    self.addPanel(width=1, height=2, gridPos=(0, 1))
    self.addPanel(width=2, height=1, gridPos=(1, 0))
    self.addPanel(width=1, height=1, gridPos=(1, 1))
    self.addPanel(width=1, height=1, gridPos=(2, 1))
    self.addPanel(width=3, height=1, gridPos=(1, 2))
    self.addPanel(width=1, height=1, gridPos=(4, 2))

  def _loadView(self):
    ship = tk.PhotoImage(file='assets/elements/ship-small.png')
    instruction = tk.PhotoImage(file='assets/elements/instruction.png')
    timer_empty = tk.PhotoImage(file='assets/elements/timer-empty.png')
    space = tk.PhotoImage(file='assets/elements/space-top.png')

    panel1x1 = tk.PhotoImage(file='assets/panels/1x1.png')
    panel1x2 = tk.PhotoImage(file='assets/panels/1x2.png')
    panel2x1 = tk.PhotoImage(file='assets/panels/2x1.png')
    panel2x2 = tk.PhotoImage(file='assets/panels/2x2.png')
    panel3x1 = tk.PhotoImage(file='assets/panels/3x1.png')

    self.panel1x1 = panel1x1
    self.panels = {
      '1x1': panel1x1,
      '1x2': panel1x2,
      '2x1': panel2x1,
      '2x2': panel2x2,
      '3x1': panel3x1
    }

    self.ship = ship
    self.instruction = instruction.zoom(3).subsample(2)
    self.timer_empty = timer_empty.zoom(3).subsample(2)
    self.space = space

    self.create_image(0, 0, image=self.space, anchor=tk.NW)
    self.create_image(400, 50, image=self.ship, tags='SHIP')

    # Instruction
    for distance in range(8):
      self.create_image(distance * 95, 100, image=self.instruction, anchor=tk.NW)

    self.create_image(0, 195, image=self.timer_empty, anchor=tk.NW)
    self.create_image(480, 195, image=self.timer_empty, anchor=tk.NW)
    self.create_text(30, 150, text='▶  Engage Elgenthrottle', fill='white', font=_getFont('heading'), anchor=tk.W)
