import tkinter as tk
import menu

from utils.fonts import _getFont
from chat.main import Chat
from ui.button import Button

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
    connectToHost = Button(
      self,
      text='Connect to Host',
      command=self.connectToHost
    )
    hostGame = Button(
      self,
      text='Host Game',
      command=self.createLobby
    )

    hostGame.pack()
    connectToHost.pack()
