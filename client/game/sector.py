import tkinter as tk

from threading import Thread
from utils.fonts import _getFont
from time import sleep
from game import Ship

class Sector(tk.Canvas):
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

    self.root.changeGameScreen(Ship)

  def _loadView(self):
    ship = tk.PhotoImage(file='assets/elements/ship-small.png')
    warning = tk.PhotoImage(file='assets/elements/warning.png')

    self.ship = ship
    self.warning = warning.subsample(2)

    self.create_rectangle(0, 0, 700, 100, fill='blue', outline='')
    self.create_image(-30, 50, image=self.ship, tags='SHIP')
    self.create_text(350, 200, font=_getFont('title2'), text='SECTOR', fill='gray')
    self.create_text(360, 280, font=_getFont('hero'), text='1', fill='white')
    self.create_rectangle(0, 420, 700, 600, fill='#1f1f1f', outline='')
    self.create_image(350, 480, image=self.warning)
    self.create_text(350, 540, font=_getFont('body3'), text='Don\'t worry, the ship flies itself.', fill='white')