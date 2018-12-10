import tkinter as tk
import menu

from utils import _getFont, colors
from ui import create_rounded_rectangle

class HowToPlay(tk.Canvas):
  def __init__(self, root):
    tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg='black')
    self.root = root

    self._loadView()

  def toggleButton_on(self, event=None):
    self.root.changeScreen(menu.Main)

  def toggleButton_off(self, event=None):
    self.itemconfig('btn', image=self.btnon)

  def _loadView(self):
    space = tk.PhotoImage(file='assets/elements/space-full.png')
    players = tk.PhotoImage(file='assets/elements/howtoplay.png')
    btnoff = tk.PhotoImage(file='assets/controls/TextButtonOff.png')
    btnon = tk.PhotoImage(file='assets/controls/TextButtonOn.png')

    self.space = space
    self.players = players.zoom(3).subsample(5)
    self.btnoff = btnoff.zoom(2).subsample(3)
    self.btnon = btnon.zoom(2).subsample(3)

    self.create_image(0, 0, image=self.space, anchor=tk.NW)
    self.create_text(500, 70, text='HOW TO PLAY', fill='white', font=_getFont('heading-2x'), anchor=tk.N)
    self.create_image(500, 220, image=self.players)
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
    self.create_text(
      500,
      435,
      text='Turn the dial to enter the waiting room. When everyone is ready,',
      fill='white',
      font=_getFont('body2')
    )
    self.create_text(
      500,
      460,
      text='hold the green button to transmit signals. Good luck, and remember',
      fill='white',
      font=_getFont('body2')
    )
    self.create_text(
      500,
      485,
      text='to work together...as a spaceteam!',
      fill='white',
      font=_getFont('body2')
    )
    self.create_image(15, 575, image=self.btnoff, tags='btn', anchor=tk.SW)
    self.create_text(45, 555, text='Back', fill='white', font=_getFont('title3'), anchor=tk.W, tags='back')

    self.tag_bind('btn', '<Button-1>', self.toggleButton_off)    
    self.tag_bind('back', '<Button-1>', self.toggleButton_off)    
    self.tag_bind('btn', '<ButtonRelease-1>', self.toggleButton_on)    
    self.tag_bind('back', '<ButtonRelease-1>', self.toggleButton_on)    
