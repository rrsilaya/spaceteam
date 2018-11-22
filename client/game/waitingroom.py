import tkinter as tk

from utils.fonts import _getFont

class WaitingRoom(tk.Frame):
  def __init__(self, root):
    self.frame = tk.Frame.__init__(self, root, width=700, height=600, background='blue')
    self.root = root

    self._loadView()

  def _loadView(self):
    exitRoom = tk.Button(
      self,
      text='BACK TO MENU',
      bg='black',
      fg='white',
      command=self.root.exitLobby,
      font=_getFont('title2')
    )

    exitRoom.pack()
