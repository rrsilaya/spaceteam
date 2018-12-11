import tkinter as tk
from utils.fonts import _getFont

Y_OFFSET = 220
PANEL_HEIGHT = 127
PANEL_WIDTH = 140

class Switch:
  def __init__(self, root, label, id, position, horizontal=True, callback=None):
    self.id = id
    self.root = root

    self.x, self.y = position
    self.label = label
    self.horizontal = horizontal
    self.callback = callback

    self.isToggled = False

    self._loadPanel()

  def toggleHSwitch(self, event=None):
    if self.isToggled:
      self.root.itemconfig(self.id, image=self.root.hswitch_off)
    else:
      self.root.itemconfig(self.id, image=self.root.hswitch_on)

    self.isToggled = not self.isToggled

    if self.callback:
      self.callback(self.isToggled)

  def toggleVSwitch(self, event=None):
    if self.isToggled:
      self.root.itemconfig(self.id, image=self.root.vswitch_off)
    else:
      self.root.itemconfig(self.id, image=self.root.vswitch_on)

    self.isToggled = not self.isToggled

    if self.callback:
      self.callback(self.isToggled)

  def _loadPanel(self):
    hswitch_off = tk.PhotoImage(file='assets/ui/horizontalswitch-off.png')
    hswitch_on = tk.PhotoImage(file='assets/ui/horizontalswitch-on.png')
    vswitch_off = tk.PhotoImage(file='assets/ui/verticalswitch-off.png')
    vswitch_on = tk.PhotoImage(file='assets/ui/verticalswitch-on.png')

    if self.horizontal and not hasattr(self.root, 'hswitch_off'):
      self.root.hswitch_off = hswitch_off.subsample(2)
      self.root.hswitch_on = hswitch_on.subsample(2)
    elif not hasattr(self.root, 'vswitch_off'):
      self.root.vswitch_off = vswitch_off.subsample(2)
      self.root.vswitch_on = vswitch_on.subsample(2)

    self.root.addPanel(width=1, height=1, gridPos=(self.x, self.y))
    self.root.create_text(
      70 + self.x * PANEL_WIDTH,
      Y_OFFSET + (45 if self.horizontal else 40) + self.y * PANEL_HEIGHT,
      text=self.label,
      fill='black',
      font=_getFont('body')
    )
    self.root.create_image(
      70 + self.x * PANEL_WIDTH,
      Y_OFFSET + (80 if self.horizontal else 75) + self.y * PANEL_HEIGHT,
      image=self.root.hswitch_off if self.horizontal else self.root.vswitch_off,
      tags=self.id
    )

    self.root.tag_bind(self.id, '<Button-1>', self.toggleHSwitch if self.horizontal else self.toggleVSwitch)
