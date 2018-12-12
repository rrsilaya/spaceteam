import tkinter as tk

from threading import Thread
from utils.fonts import _getFont
from time import sleep

class Lose(tk.Canvas):
  def __init__(self, root):
    tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg='black')
    self.root = root

    self._loadView()
    Thread(target=self.animateShip).start()

  def animateShip(self):
    sleep(4)
    self.root.exitLobby()

  def _loadView(self):
    icon = tk.PhotoImage(file='assets/elements/CharacterCreatorIcon.png')
    space = tk.PhotoImage(file='assets/elements/space-top.png')

    sun = tk.PhotoImage(file='assets/elements/Sun.png')

    self.icon = icon.subsample(3)
    self.space = space
    self.sun = sun.zoom(3)

    self.create_image(0, 0, image=self.space, anchor=tk.NW)

    self.create_image(350, 220, image=self.sun)
    self.create_text(350, 350, font=_getFont('heading-2x'), fill='white', text='YOU JUST CRASHED!')

    self.create_rectangle(0, 420, 700, 600, fill='#1f1f1f', outline='')
    self.create_image(350, 480, image=self.icon)
    self.create_text(350, 545, font=_getFont('body3'), text='In memory of the brave people in this expedition', fill='white')