import tkinter as tk
import menu
from utils.fonts import _getFont

class Main(tk.Frame):
  def __init__(self, root):
    self.frame = tk.Frame.__init__(self, root, background='black')
    self.root = root

    self._loadView()

  def createNewGame(self):
    self.root.changeScreen(menu.Connect)

  def _loadView(self):
    newGame = tk.Button(
      self,
      text='New Game',
      height=1,
      width=15,
      font=_getFont('title'),
      command=self.createNewGame
    )

    newGame.pack()
