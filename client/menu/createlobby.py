import tkinter as tk
import menu

from utils.fonts import _getFont
from chat.main import Chat

class CreateLobby(tk.Frame):
  def __init__(self, root):
    self.frame = tk.Frame.__init__(self, root, background='black')
    self.root = root

    self._loadView()
    self.createLobby()

  def createLobby(self):
    self.root.chat = Chat()
    self.root.createdLobby = self.root.chat.createLobby(5)
    self.root.changeScreen(menu.Connect)

  def _loadView(self):
    connecting = tk.Label(
      self,
      text='Creating Lobby',
      fg='white',
      bg='black',
      font=_getFont('title')
    )

    connecting.place(x=500, y=300, anchor='center')
