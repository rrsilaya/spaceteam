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
    self.background = tk.PhotoImage(file='assets/background/main.png')
    background = tk.Label(self, image=self.background)

    connectToHost = Button(
      self,
      text='Connect to Host',
      bg='gray',
      command=self.connectToHost
    )
    hostGame = Button(
      self,
      text='Host Game',
      bg='gray',
      command=self.createLobby
    )

    background.place(x=0, y=0, relwidth=1, relheight=1)
    hostGame.place(x=500, y=350, anchor=tk.CENTER)
    connectToHost.place(x=500, y=450, anchor=tk.CENTER)
