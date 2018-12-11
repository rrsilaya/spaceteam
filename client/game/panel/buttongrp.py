import tkinter as tk
from utils.fonts import _getFont

Y_OFFSET = 220
PANEL_HEIGHT = 127
PANEL_WIDTH = 140

class ButtonGroup:
  def __init__(self, root, label, id, position, buttons, callback=None):
    self.id = id
    self.root = root

    self.x, self.y = position
    self.label = label
    self.buttons = buttons
    self.callback = callback

    self._loadPanel()

  def toggleButton(self, tag, flag):
    if flag:
      self.root.itemconfig(tag, image=self.root.btn_on)
    else:
      self.root.itemconfig(tag, image=self.root.btn_off)

  def _loadPanel(self):
    btn_off = tk.PhotoImage(file='assets/controls/TextButtonOff.png')
    btn_on = tk.PhotoImage(file='assets/controls/TextButtonOn.png')

    if not hasattr(self.root, 'btn_off'):
      self.root.btn_off = btn_off
      self.root.btn_on = btn_on

    self.root.addPanel(width=2, height=2, gridPos=(self.x, self.y))
    self.root.create_text(145 + PANEL_WIDTH * self.x, Y_OFFSET + 50 + PANEL_HEIGHT * self.y, text=self.label, fill='black', font=_getFont('body'))
    self.root.create_image(145 + PANEL_WIDTH * self.x, Y_OFFSET + 105 + PANEL_HEIGHT * self.y, image=self.root.btn_off, tags='{}1'.format(self.id))
    self.root.create_image(145 + PANEL_WIDTH * self.x, Y_OFFSET + 180 + PANEL_HEIGHT * self.y, image=self.root.btn_off, tags='{}2'.format(self.id))
    self.root.create_text(145 + PANEL_WIDTH * self.x, Y_OFFSET + 105 + PANEL_HEIGHT * self.y, text=self.buttons[0], fill='white', font=_getFont('heading-2s'), tags='{}1L'.format(self.id))
    self.root.create_text(145 + PANEL_WIDTH * self.x, Y_OFFSET + 180 + PANEL_HEIGHT * self.y, text=self.buttons[1], fill='white', font=_getFont('heading-2s'), tags='{}2L'.format(self.id))

    self.root.tag_bind('{}1'.format(self.id), '<Button-1>', lambda _: self.toggleButton('{}1'.format(self.id), True))
    self.root.tag_bind('{}1'.format(self.id), '<ButtonRelease-1>', lambda _: self.toggleButton('{}1'.format(self.id), False))
    self.root.tag_bind('{}2'.format(self.id), '<Button-1>', lambda _: self.toggleButton('{}2'.format(self.id), True))
    self.root.tag_bind('{}2'.format(self.id), '<ButtonRelease-1>', lambda _: self.toggleButton('{}2'.format(self.id), False))
    self.root.tag_bind('{}1L'.format(self.id), '<Button-1>', lambda _: self.toggleButton('{}1'.format(self.id), True))
    self.root.tag_bind('{}1L'.format(self.id), '<ButtonRelease-1>', lambda _: self.toggleButton('{}1'.format(self.id), False))
    self.root.tag_bind('{}2L'.format(self.id), '<Button-1>', lambda _: self.toggleButton('{}2'.format(self.id), True))
    self.root.tag_bind('{}2L'.format(self.id), '<ButtonRelease-1>', lambda _: self.toggleButton('{}2'.format(self.id), False))
