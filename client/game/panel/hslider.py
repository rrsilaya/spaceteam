import tkinter as tk
from utils.fonts import _getFont

Y_OFFSET = 220
PANEL_HEIGHT = 127
PANEL_WIDTH = 140

class HorizontalSlider:
  def __init__(self, root, label, id, position, callback=None):
    self.id = id
    self.root = root

    self.x, self.y = position
    self.label = label
    self.index = 0
    self.callback = callback

    self._loadPanel()

  def handleHSlider(self, event):
    c = self.root.coords('{}_GUIDE'.format(self.id))

    start = c[0]
    end = c[2]
    interval = end - start

    if event.x <= start:
      coord = start
    elif event.x >= end:
      coord = end
    else:
      coord = event.x

    ct = self.root.coords(self.id)
    self.root.coords(self.id, coord, ct[1])

  def handleHSliderDrop(self, event):
    c = self.root.coords('{}_GUIDE'.format(self.id))

    start = c[0]
    end = c[2]
    interval = end - start
    multiplier = interval / 4

    if event.x <= start:
      index = 0
    elif event.x >= end:
      index = 4
    else:
      index = round((event.x - start) / multiplier)

    ct = self.root.coords(self.id)
    self.root.coords(self.id, start + (index * multiplier), ct[1])
    self.index = index

  def _loadPanel(self):
    hslider = tk.PhotoImage(file='assets/controls/SliderH.png')

    if not hasattr(self.root, 'hslider'):
      self.root.hslider = hslider

    self.root.create_text(210 + PANEL_WIDTH * self.x, Y_OFFSET + 36 + PANEL_HEIGHT * self.y, text=self.label, fill='black', font=_getFont('body'))
    self.root.create_rectangle(60 + PANEL_WIDTH * self.x, Y_OFFSET + 63 + PANEL_HEIGHT * self.y, 360 + PANEL_WIDTH * self.x, Y_OFFSET + 68 + PANEL_HEIGHT * self.y, fill='black', outline='', tags='{}_GUIDE'.format(self.id))
    self.root.create_image(60 + PANEL_WIDTH * self.x, Y_OFFSET + 66 + PANEL_HEIGHT * self.y, image=self.root.hslider, tags=self.id)
    for i in range(5): self.root.create_text(60 + PANEL_WIDTH * self.x + (i * 75), Y_OFFSET + 101 + PANEL_HEIGHT * self.y, text=str(i), fill='black', font=_getFont('body3'))

    self.root.tag_bind(self.id, '<B1-Motion>', self.handleHSlider)
    self.root.tag_bind(self.id, '<ButtonRelease-1>', self.handleHSliderDrop)
