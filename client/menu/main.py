import tkinter as tk
import menu

from PIL import Image, ImageTk
from utils import _getFont, colors
from chat.main import Chat

class Main(tk.Canvas):
  def __init__(self, root):
    tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg='black')
    self.root = root

    self.isHost = True
    self.dialRotation = 110

    self._loadView()

  def toggleChat(self, event=None):
    if self.root.enableChat:
      self.itemconfig('CHAT_SWITCH', image=self.switch_off)
    else:
      self.itemconfig('CHAT_SWITCH', image=self.switch_on)

    self.root.enableChat = not self.root.enableChat

  def toggleMode(self, event=None):
    if self.isHost:
      self.itemconfig('MODE_SWITCH', image=self.vswitch_off)
    else:
      self.itemconfig('MODE_SWITCH', image=self.vswitch_on)

    self.isHost = not self.isHost

  def handleDial(self, event=None):
    range = (420, 575) # 155
    rotation = (110, -100) # 210deg
    self.dialRotation = int(((event.x - range[0]) / 155) * 210)

    if self.dialRotation < 0:
      self.dialRotation = 0
    elif self.dialRotation > 210:
      self.dialRotation = 210

    self.dial = ImageTk.PhotoImage(self.dial_image.rotate(rotation[0] - self.dialRotation, expand=True))
    self.itemconfig('DIAL', image=self.dial)

  def handleDialRelease(self, event=None):
    if self.dialRotation == 210:
      if self.isHost:
        self.root.changeScreen(menu.Connecting)
      else:
        self.root.changeScreen(menu.Connect)

  def handleBtn_off(self, event=None):
    self.itemconfig('HELP', image=self.btn_on)

  def handleBtn_on(self, event=None):
    self.root.changeScreen(menu.HowToPlay)

  def _loadView(self):
    logo = tk.PhotoImage(file='assets/ui/logo.png')
    space = tk.PhotoImage(file='assets/elements/space-full.png')
    switch_off = tk.PhotoImage(file='assets/ui/horizontalswitch-off.png')
    switch_on = tk.PhotoImage(file='assets/ui/horizontalswitch-on.png')
    vswitch_off = tk.PhotoImage(file='assets/ui/verticalswitch-off.png')
    vswitch_on = tk.PhotoImage(file='assets/ui/verticalswitch-on.png')
    btn_off = tk.PhotoImage(file='assets/controls/green-off.png')
    btn_on = tk.PhotoImage(file='assets/controls/green-on.png')
    dial = Image.open('assets/ui/dial.png')

    self.logo = logo
    self.space = space
    self.switch_off = switch_off.subsample(2)
    self.switch_on = switch_on.subsample(2)
    self.vswitch_off = vswitch_off.subsample(2)
    self.vswitch_on = vswitch_on.subsample(2)
    self.btn_off = btn_off.zoom(2).subsample(3)
    self.btn_on = btn_on.zoom(2).subsample(3)

    self.dial_image = dial.resize((int(dial.size[0] * 1.15), int(dial.size[1] * 1.15)))
    self.dial = ImageTk.PhotoImage(self.dial_image.rotate(110, expand=True))

    self.create_image(0, 0, image=self.space, anchor=tk.NW)
    self.create_image(500, 150, image=self.logo)
    self.create_text(500, 250, text='SPACETEAM', fill='white', font=_getFont('heading-3x'))
    self.create_image(500, 430, image=self.dial, tags='DIAL')
    self.create_text(625, 440, text='PLAY', fill='white', font=_getFont('body4'))

    self.create_text(113, 530, text='IN-GAME CHAT', fill=colors.GREEN, font=_getFont('body2'))
    self.create_text(40, 565, text='OFF', fill='white', font=_getFont('body2'))
    self.create_image(70, 563, image=self.switch_on, anchor=tk.W, tags='CHAT_SWITCH')
    self.create_text(180, 565, text='ON', fill='white', font=_getFont('body2'))

    self.create_text(960, 25, text='HOST', fill='white', font=_getFont('body2'))
    self.create_image(959, 35, image=self.vswitch_on, anchor=tk.N, tags='MODE_SWITCH')
    self.create_text(960, 155, text='JOIN', fill='white', font=_getFont('body2'))

    self.create_image(985, 585, image=self.btn_off, anchor=tk.SE, tags='HELP')
    self.create_text(955, 565, text='Help', fill='white', font=_getFont('title3'), anchor=tk.E, tags='HELP_TEXT')

    self.tag_bind('CHAT_SWITCH', '<ButtonPress-1>', self.toggleChat)
    self.tag_bind('MODE_SWITCH', '<ButtonPress-1>', self.toggleMode)
    self.tag_bind('DIAL', '<B1-Motion>', self.handleDial)
    self.tag_bind('DIAL', '<ButtonRelease-1>', self.handleDialRelease)
    self.tag_bind('HELP', '<ButtonPress-1>', self.handleBtn_off)
    self.tag_bind('HELP_TEXT', '<ButtonPress-1>', self.handleBtn_off)
    self.tag_bind('HELP', '<ButtonRelease-1>', self.handleBtn_on)
    self.tag_bind('HELP_TEXT', '<ButtonRelease-1>', self.handleBtn_on)
