import tkinter as tk
import menu
import chat

from game import WaitingRoom

class Lobby(tk.Frame):
  def __init__(self, root):
    self.frame = tk.Frame.__init__(self, root, background='black')
    self.root = root

    self._loadView()

  def changeGameScreen(self, screen):
    before = self.game
    before.destroy()

    self.game = screen(self)
    self.game.pack(side=tk.LEFT)

  def exitLobby(self):
    self.root.chat.disconnect()
    self.root.chat = None
    
    self.chatbox.destroy()
    self.game.destroy()
    self.root.changeScreen(menu.Main)

  def _loadView(self):
    self.chatbox = chat.Screen(self.root)
    self.game = WaitingRoom(self)

    self.chatbox.pack(side=tk.RIGHT)
    self.game.pack(side=tk.LEFT)
