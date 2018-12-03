import tkinter as tk
import menu

from re import match
from utils.fonts import _getFont

class GetIp(tk.Frame):
  def __init__(self, root):
    self.frame = tk.Frame.__init__(self, root, background='black')
    self.root = root

    self.ipaddr = tk.StringVar()
    self.ipaddr.trace('w', self._restrictIpAddress)

    self._loadView()

  def connectToServer(self, event=None):
    print('Connecting to {}'.format(self.ipaddr.get()))
    self.root.changeScreen(menu.Main)

  def _restrictIpAddress(self, *args):
    value = self.ipaddr.get()
    limit = 15

    if len(value) <= limit:
      if (not match(r'^[0-9\.]+$', value)) or value.count('.') > 3:
        self.ipaddr.set(value[:len(value) - 1])
    else:
      self.ipaddr.set(value[:limit])

  def _loadView(self):
    inputField = tk.Entry(
      self,
      textvariable=self.ipaddr,
      bg='black',
      fg='white',
      highlightcolor='white',
      justify=tk.CENTER,
      font=_getFont('title2')
    )
    fieldLabel = tk.Label(
      self,
      text='ENTER SERVER IP ADDRESS',
      bg='black',
      fg='white',
      font=_getFont('body')
    )

    fieldLabel.place(x=500, y=335, anchor='center')
    inputField.place(x=500, y=285, height=60, anchor='center')
    inputField.focus()
    inputField.bind('<Return>', self.connectToServer)
