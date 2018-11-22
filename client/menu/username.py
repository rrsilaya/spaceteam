import tkinter as tk
from utils.fonts import _getFont

import menu

class Username(tk.Frame):
  def __init__(self, root):
    self.frame = tk.Frame.__init__(self, root, background='black')
    self.root = root

    self.username = tk.StringVar()
    self.username.trace('w', self._restrictMaxChars)

    self._loadView()

  def setUsername(self, event=None):
    username = self.username.get()
    self.root.username = username

    self.root.changeScreen(menu.Main)

  def _restrictMaxChars(self, *args):
    limit = 18
    value = self.username.get()

    if len(value) > limit:
      self.username.set(value[:limit])

  def _loadView(self):
    inputField = tk.Entry(
      self,
      textvariable=self.username,
      bg='black',
      fg='white',
      highlightcolor='white',
      justify=tk.CENTER,
      font=_getFont('title2')
    )
    fieldLabel = tk.Label(
      self,
      text='ENTER USERNAME',
      bg='black',
      fg='white',
      font=_getFont('body')
    )

    fieldLabel.place(x=500, y=335, anchor='center')
    inputField.place(x=500, y=285, height=60, anchor='center')
    inputField.focus()
    inputField.bind('<Return>', self.setUsername)
