import tkinter as tk

from threading import Thread
from utils.fonts import _getFont
from time import sleep

class Win(tk.Canvas):
  def __init__(self, root):
    tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg='black')
    self.root = root

    self._loadView()
    Thread(target=self.animateShip).start()

  def animateShip(self):
    sleep(0.5)
    for distance in range(405):
      self.move('SHIP', 2, 0)
      sleep(0.01)

    sleep(2)
    self.root.exitLobby()

  def _loadView(self):
    ship = tk.PhotoImage(file='assets/elements/ship-small.png')
    icon = tk.PhotoImage(file='assets/elements/MedalIcon.png')
    space = tk.PhotoImage(file='assets/elements/space-top.png')

    medal = tk.PhotoImage(file='assets/elements/MedalIconFull.png')
    wreath = tk.PhotoImage(file='assets/elements/Wreath.png')

    self.ship = ship
    self.icon = icon.subsample(2)
    self.space = space
    self.medal = medal.zoom(3).subsample(2)
    self.wreath = wreath.subsample(2)

    self.create_image(0, 0, image=self.space, anchor=tk.NW)
    self.create_image(-30, 50, image=self.ship, tags='SHIP')

    self.create_image(350, 220, image=self.wreath)
    self.create_image(350, 200, image=self.medal)
    self.create_text(350, 330, font=_getFont('heading-2x'), fill='white', text='CONGRATULATIONS!')

    self.create_rectangle(0, 420, 700, 600, fill='#1f1f1f', outline='')
    self.create_image(350, 480, image=self.icon)
    self.create_text(350, 545, font=_getFont('body3'), text='You have what it takes to be in a spaceteam!', fill='white')