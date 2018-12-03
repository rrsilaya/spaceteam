import tkinter as tk
import menu

from utils import _getFont, colors
from ui import create_rounded_rectangle
from threading import Thread
from time import sleep

class Welcome(tk.Canvas):
  def __init__(self, root):
    tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg=colors.DBLUE)
    self.root = root

    self.time = 0
    Thread(target=self.updateTimeout).start()

    self._loadView()

  def updateTimeout(self):
    while self.time < 4:
      sleep(1)
      self.time += 1

    self.root.changeScreen(menu.GetIp)

  def _loadView(self):
    players = tk.PhotoImage(file='assets/elements/howtoplay.png')

    self.players = players.zoom(3).subsample(5)

    self.create_image(500, 210, image=self.players)
    self.create_text(
      500,
      350,
      text='Spaceteam is a cooperative game played with 2-8 people in the',
      fill=colors.GREEN,
      font=_getFont('body2')
    )
    self.create_text(
      500,
      375,
      text='same network. Each player needs his/her device connected.',
      fill=colors.GREEN,
      font=_getFont('body2')
    )
    create_rounded_rectangle(self, 175, 320, 825, 400, r=10, fill='', outline=colors.GREEN)
