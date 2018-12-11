import tkinter as tk
from utils.fonts import _getFont

Y_OFFSET = 220
PANEL_HEIGHT = 127
PANEL_WIDTH = 140

class VerticalSlider:
  def __init__(self, root, label, id, position, callback=None):
    self.id = id
    self.root = root

    self.x, self.y = position
    self.label = label
    self.index = 0
    self.callback = callback

    self._loadPanel()

  def _sendPacket(self):
    packet = self.root.udpPacket

    payload = packet.CommandPacket()
    payload.type = packet.COMMAND
    payload.command = self.id
    payload.panel = str(self.index)

    self.root.gameConnection.send(payload)

  def handleVSlider(self, event):
    c = self.root.coords('{}_GUIDE'.format(self.id))

    start = c[1]
    end = c[3]
    interval = end - start

    if event.y <= start:
      coord = start
    elif event.y >= end:
      coord = end
    else:
      coord = event.y

    ct = self.root.coords(self.id)
    self.root.coords(self.id, ct[0], coord)

  def handleVSliderDrop(self, event):
    c = self.root.coords('{}_GUIDE'.format(self.id))

    start = c[1]
    end = c[3]
    interval = end - start
    multiplier = interval / 2

    if event.y <= start:
      index = 0
    elif event.y >= end:
      index = 2
    else:
      index = round((event.y - start) / multiplier)

    ct = self.root.coords(self.id)
    self.root.coords(self.id, ct[0], start + (index * multiplier))
    self.index = index
    self._sendPacket()

  def _loadPanel(self):
    vslider = tk.PhotoImage(file='assets/controls/SliderV.png')

    if not hasattr(self.root, 'vslider'):
      self.root.vslider = vslider

    self.root.addPanel(width=1, height=2, gridPos=(self.x, self.y))
    self.root.create_text(70 + PANEL_WIDTH * self.x, Y_OFFSET + 28 + PANEL_HEIGHT * self.y, text=self.label, fill='black', font=_getFont('body'))
    self.root.create_rectangle(68 + PANEL_WIDTH * self.x, Y_OFFSET + 98 + PANEL_HEIGHT * self.y, 73 + PANEL_WIDTH * self.x, Y_OFFSET + 208 + PANEL_HEIGHT * self.y, fill='black', outline='', tags='{}_GUIDE'.format(self.id))
    self.root.create_image(70 + PANEL_WIDTH * self.x, Y_OFFSET + 88 + PANEL_HEIGHT * self.y, image=self.root.vslider, tags=self.id)

    for i in range(3):
      self.root.create_text(35 + PANEL_WIDTH * self.x, Y_OFFSET + 88 + PANEL_HEIGHT * self.y + (i * 60), text=str(i), fill='black', font=_getFont('body3'))

    self.root.tag_bind(self.id, '<B1-Motion>', self.handleVSlider)
    self.root.tag_bind(self.id, '<ButtonRelease-1>', self.handleVSliderDrop)
