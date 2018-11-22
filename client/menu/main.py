import tkinter as tk
import menu

from utils.fonts import _getFont
from chat.main import Chat

class Main(tk.Frame):
  def __init__(self, root):
    self.frame = tk.Frame.__init__(self, root, background='black')
    self.root = root

    self._loadView()

  def connectToHost(self):
    self.root.changeScreen(menu.Connect)

  def createLobby(self):
    self.root.chat = Chat()

    chatroom = self.root.chat.createLobby(5)
    
    self.root.chat.connect(chatroom, self.root.username)
    self.root.changeScreen(menu.Lobby)

  def _loadView(self):
    connectToHost = tk.Button(
      self,
      text='Connect to Host',
      height=1,
      width=15,
      font=_getFont('title'),
      command=self.connectToHost
    )
    hostGame = tk.Button(
      self,
      text='Host Game',
      height=1,
      width=15,
      font=_getFont('title'),
      command=self.createLobby
    )

    hostGame.pack()
    connectToHost.pack()
