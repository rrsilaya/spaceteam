import tkinter as tk

import chat

class Lobby(tk.Frame):
  def __init__(self, root):
    self.frame = tk.Frame.__init__(self, root, background='red')
    self.root = root

    self._loadView()

  def _loadView(self):
    chatbox = chat.Screen(self.root)

    chatbox.pack(side=tk.RIGHT)