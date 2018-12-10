import tkinter as tk
from utils.fonts import _getFont

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

    self.addPanel(width=2, height=2, gridPos=(3, 0))
    self.addPanel(width=1, height=1, gridPos=(0, 0))
    self.addPanel(width=1, height=2, gridPos=(0, 1))
    self.addPanel(width=2, height=1, gridPos=(1, 0))
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

  def toggleVSwitch(self, tag):
    if self.controls[tag]:
      self.itemconfig(tag, image=self.vswitch_off)
    else:
      self.itemconfig(tag, image=self.vswitch_on)

    self.controls[tag] = not self.controls[tag]

  def toggleHSwitch(self, tag):
    if self.controls[tag]:
      self.itemconfig(tag, image=self.hswitch_off)
    else:
      self.itemconfig(tag, image=self.hswitch_on)

    self.controls[tag] = not self.controls[tag]

  def toggleBoxButton(self, tag, flag):
    if flag:
      self.itemconfig(tag, image=self.box_on)
    else:
      self.itemconfig(tag, image=self.box_off)

  def toggleButton(self, tag, flag):
    if flag:
      self.itemconfig(tag, image=self.btn_on)
    else:
      self.itemconfig(tag, image=self.btn_off)

  def handleHSlider(self, tag, guide, event):
    c = self.coords(guide)

    start = c[0]
    end = c[2]
    interval = end - start

    if event.x <= start:
      coord = start
    elif event.x >= end:
      coord = end
    else:
      coord = event.x

    ct = self.coords(tag)
    self.coords(tag, coord, ct[1])

  def handleHSliderDrop(self, tag, guide, intervals, event):
    c = self.coords(guide)

    start = c[0]
    end = c[2]
    interval = end - start
    multiplier = interval / intervals

    if event.x <= start:
      index = 0
    elif event.x >= end:
      index = intervals
    else:
      index = round((event.x - start) / multiplier)

    ct = self.coords(tag)
    self.coords(tag, start + (index * multiplier), ct[1])

  def handleVSlider(self, tag, guide, event):
    c = self.coords(guide)

    start = c[1]
    end = c[3]
    interval = end - start

    if event.y <= start:
      coord = start
    elif event.y >= end:
      coord = end
    else:
      coord = event.y

    ct = self.coords(tag)
    self.coords(tag, ct[0], coord)

  def handleVSliderDrop(self, tag, guide, intervals, event):
    c = self.coords(guide)

    start = c[1]
    end = c[3]
    interval = end - start
    multiplier = interval / intervals

    if event.y <= start:
      index = 0
    elif event.y >= end:
      index = intervals
    else:
      index = round((event.y - start) / multiplier)

    ct = self.coords(tag)
    self.coords(tag, ct[0], start + (index * multiplier))

  def _prepareControls(self):
    vswitch_off = tk.PhotoImage(file='assets/ui/verticalswitch-off.png')
    vswitch_on = tk.PhotoImage(file='assets/ui/verticalswitch-on.png')
    hswitch_off = tk.PhotoImage(file='assets/ui/horizontalswitch-off.png')
    hswitch_on = tk.PhotoImage(file='assets/ui/horizontalswitch-on.png')
    btn_off = tk.PhotoImage(file='assets/controls/TextButtonOff.png')
    btn_on = tk.PhotoImage(file='assets/controls/TextButtonOn.png')
    hslider = tk.PhotoImage(file='assets/controls/SliderH.png')
    vslider = tk.PhotoImage(file='assets/controls/SliderV.png')
    box_off = tk.PhotoImage(file='assets/controls/red-off.png')
    box_on = tk.PhotoImage(file='assets/controls/red-on.png')

    self.vswitch_off = vswitch_off.subsample(2)
    self.vswitch_on = vswitch_on.subsample(2)
    self.hswitch_off = hswitch_off.subsample(2)
    self.hswitch_on = hswitch_on.subsample(2)
    self.btn_off = btn_off
    self.btn_on = btn_on
    self.hslider = hslider
    self.vslider = vslider
    self.box_off = box_off
    self.box_on = box_on

    self.create_image(70, Y_OFFSET + 63, image=self.hswitch_off, tags='HSWITCH1')
    self.create_image(565, Y_OFFSET + 105, image=self.btn_off, tags='BTN1')
    self.create_image(565, Y_OFFSET + 180, image=self.btn_off, tags='BTN2')

    self.create_rectangle(200, Y_OFFSET + 322, 500, Y_OFFSET + 327, fill='black', outline='', tags='HSLIDER_GUIDE')
    self.create_image(200, Y_OFFSET + 325, image=self.hslider, tags='HSLIDER')

    self.create_image(295, Y_OFFSET + 64, image=self.box_off, tags='BOX1')
    self.create_image(370, Y_OFFSET + 64, image=self.box_off, tags='BOX2')

    self.create_rectangle(68, Y_OFFSET + 225, 73, 555, fill='black', outline='', tags='VSLIDER_GUIDE')
    self.create_image(70, Y_OFFSET + 215, image=self.vslider, tags='VSLIDER')

    self.create_image(350, Y_OFFSET + 190, image=self.vswitch_off, tags='VSWITCH1')

    self.tag_bind('HSWITCH1', '<Button-1>', lambda _: self.toggleHSwitch('HSWITCH1'))
    self.tag_bind('VSWITCH1', '<Button-1>', lambda _: self.toggleVSwitch('VSWITCH1'))

    self.tag_bind('BOX1', '<Button-1>', lambda _: self.toggleBoxButton('BOX1', True))
    self.tag_bind('BOX1', '<ButtonRelease-1>', lambda _: self.toggleBoxButton('BOX1', False))
    self.tag_bind('BOX2', '<Button-1>', lambda _: self.toggleBoxButton('BOX2', True))
    self.tag_bind('BOX2', '<ButtonRelease-1>', lambda _: self.toggleBoxButton('BOX2', False))

    self.tag_bind('BTN1', '<Button-1>', lambda _: self.toggleButton('BTN1', True))
    self.tag_bind('BTN1', '<ButtonRelease-1>', lambda _: self.toggleButton('BTN1', False))
    self.tag_bind('BTN2', '<Button-1>', lambda _: self.toggleButton('BTN2', True))
    self.tag_bind('BTN2', '<ButtonRelease-1>', lambda _: self.toggleButton('BTN2', False))

    self.tag_bind('HSLIDER', '<B1-Motion>', lambda e: self.handleHSlider('HSLIDER', 'HSLIDER_GUIDE', e))
    self.tag_bind('HSLIDER', '<ButtonRelease-1>', lambda e: self.handleHSliderDrop('HSLIDER', 'HSLIDER_GUIDE', 4, e))
    self.tag_bind('VSLIDER', '<B1-Motion>', lambda e: self.handleVSlider('VSLIDER', 'VSLIDER_GUIDE', e))
    self.tag_bind('VSLIDER', '<ButtonRelease-1>', lambda e: self.handleVSliderDrop('VSLIDER', 'VSLIDER_GUIDE', 2, e))