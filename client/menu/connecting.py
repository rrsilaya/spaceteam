import tkinter as tk
import menu

from utils import _getFont

class Connecting(tk.Canvas):
  def __init__(self, root):
    tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg='black')
    self.root = root

    self._loadView()

  def toggleButton_on(self, event=None):
    self.create_image(500, 370, image=self.button_toggle, tags='CANCEL')
    self.create_text(500, 370, text='Cancel', fill='black', font=_getFont('title3'), tags='CANCEL_TEXT')
  
  def toggleButton_off(self, event=None):
    self.root.changeScreen(menu.Main)

  def _loadView(self):
    loading = tk.PhotoImage(file='assets/elements/searching.png')
    button = tk.PhotoImage(file='assets/ui/text-button.png')
    button_toggle = tk.PhotoImage(file='assets/ui/text-button-toggle.png')

    self.loading = loading.zoom(3).subsample(2)
    self.button = button
    self.button_toggle = button_toggle

    self.create_image(500, 160, image=self.loading)
    self.create_text(500, 230, text='SEARCHING FOR SPACETEAM SIGNALS...', fill='white', font=_getFont('heading'))
    self.create_image(500, 370, image=self.button, tags='CANCEL')
    self.create_text(500, 370, text='Cancel', fill='black', font=_getFont('title3'), tags='CANCEL_TEXT')
    self.create_text(500, 430, text='Make sure that you\'ve provided the correct channel!', fill='gray', font=_getFont('body2'))

    self.tag_bind('CANCEL', '<Button-1>', self.toggleButton_on)
    self.tag_bind('CANCEL_TEXT', '<Button-1>', self.toggleButton_on)
    self.tag_bind('CANCEL', '<ButtonRelease-1>', self.toggleButton_off)
    self.tag_bind('CANCEL_TEXT', '<ButtonRelease-1>', self.toggleButton_off)
