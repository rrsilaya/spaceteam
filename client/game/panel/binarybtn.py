import tkinter as tk
from utils.fonts import _getFont
from re import search

Y_OFFSET = 220
PANEL_HEIGHT = 127
PANEL_WIDTH = 140

class BinaryButton:
  def __init__(self, root, label, id, position, callback=None):
    self.id = id
    self.root = root

    self.x, self.y = position
    self.label = label
    self.callback = callback

    self._loadPanel()

  def _sendPacket(self, tag):
    packet = self.root.udpPacket
    panel = int(search(r'([12])L?$', tag)[1])

    payload = packet.CommandPacket()
    payload.type = packet.COMMAND
    payload.command = self.id
    payload.panel = str(panel - 1)

    self.root.gameConnection.send(payload)

  def toggleButton(self, tag, flag):
    if flag:
      self.root.itemconfig(tag, image=self.root.box_on)
    else:
      self.root.itemconfig(tag, image=self.root.box_off)
      self._sendPacket(tag)

  def _loadPanel(self):
    box_off = tk.PhotoImage(file='assets/controls/red-off.png')
    box_on = tk.PhotoImage(file='assets/controls/red-on.png')

    if not hasattr(self.root, 'box_off'):
      self.root.box_off = box_off
      self.root.box_on = box_on

    text = self.label.split(' ')

    self.root.addPanel(width=2, height=1, gridPos=(self.x, self.y))
    self.root.create_text(
      65 + PANEL_WIDTH * self.x,
      Y_OFFSET + 60 + PANEL_HEIGHT * self.y,
      text=text[0],
      fill='black',
      font=_getFont('body')
    )
    self.root.create_text(
      65 + PANEL_WIDTH * self.x,
      Y_OFFSET + 75 + PANEL_HEIGHT * self.y,
      text=text[1],
      fill='black',
      font=_getFont('body')
    )
    self.root.create_image(
      155 + PANEL_WIDTH * self.x,
      Y_OFFSET + 64 + PANEL_HEIGHT * self.y,
      image=self.root.box_off,
      tags='{}1'.format(self.id)
    )
    self.root.create_image(
      230 + PANEL_WIDTH * self.x,
      Y_OFFSET + 64 + PANEL_HEIGHT * self.y,
      image=self.root.box_off,
      tags='{}2'.format(self.id)
    )
    self.root.create_text(
      155 + PANEL_WIDTH * self.x,
      Y_OFFSET + 64 + PANEL_HEIGHT * self.y,
      text='0',
      fill='white',
      font=_getFont('heading-2x'),
      tags='{}1L'.format(self.id)
    )
    self.root.create_text(
      230 + PANEL_WIDTH * self.x,
      Y_OFFSET + 64 + PANEL_HEIGHT * self.y,
      text='1',
      fill='white',
      font=_getFont('heading-2x'),
      tags='{}2L'.format(self.id)
    )

    self.root.tag_bind('{}1'.format(self.id), '<Button-1>', lambda _: self.toggleButton('{}1'.format(self.id), True))
    self.root.tag_bind('{}1'.format(self.id), '<ButtonRelease-1>', lambda _: self.toggleButton('{}1'.format(self.id), False))
    self.root.tag_bind('{}2'.format(self.id), '<Button-1>', lambda _: self.toggleButton('{}2'.format(self.id), True))
    self.root.tag_bind('{}2'.format(self.id), '<ButtonRelease-1>', lambda _: self.toggleButton('{}2'.format(self.id), False))
    self.root.tag_bind('{}1L'.format(self.id), '<Button-1>', lambda _: self.toggleButton('{}1'.format(self.id), True))
    self.root.tag_bind('{}1L'.format(self.id), '<ButtonRelease-1>', lambda _: self.toggleButton('{}1'.format(self.id), False))
    self.root.tag_bind('{}2L'.format(self.id), '<Button-1>', lambda _: self.toggleButton('{}2'.format(self.id), True))
    self.root.tag_bind('{}2L'.format(self.id), '<ButtonRelease-1>', lambda _: self.toggleButton('{}2'.format(self.id), False))
