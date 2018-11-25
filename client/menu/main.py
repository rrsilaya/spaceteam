import tkinter as tk
import menu

from PIL import Image, ImageTk
from utils import _getFont, colors
from chat.main import Chat

class Main(tk.Canvas):
  def __init__(self, root):
    tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg='black')
    self.root = root

    self.enableChat = True
    self.isHost = True
    self.dialRotation = 110

    self._loadView()

  def toggleChat(self, event=None):
    self.delete('CHAT_SWITCH')

    if self.enableChat:
      self.create_image(70, 563, image=self.switch_off, anchor=tk.W, tags='CHAT_SWITCH')
    else:
      self.create_image(70, 563, image=self.switch_on, anchor=tk.W, tags='CHAT_SWITCH')

    self.enableChat = not self.enableChat

  def toggleMode(self, event=None):
    self.delete('MODE_SWITCH')

    if self.isHost:
      self.create_image(959, 35, image=self.vswitch_off, anchor=tk.N, tags='MODE_SWITCH')
    else:
      self.create_image(959, 35, image=self.vswitch_on, anchor=tk.N, tags='MODE_SWITCH')

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
    self.create_image(500, 430, image=self.dial, tags='DIAL')

  def handleDialRelease(self, event=None):
    if self.dialRotation == 210:
      if self.isHost:
        pass
      else:
        self.root.changeScreen(menu.Connect)

  def _loadView(self):
    logo = tk.PhotoImage(file='assets/ui/logo.png')
    switch_off = tk.PhotoImage(file='assets/ui/horizontalswitch-off.png')
    switch_on = tk.PhotoImage(file='assets/ui/horizontalswitch-on.png')
    vswitch_off = tk.PhotoImage(file='assets/ui/verticalswitch-off.png')
    vswitch_on = tk.PhotoImage(file='assets/ui/verticalswitch-on.png')
    dial = Image.open('assets/ui/dial.png')

    self.logo = logo
    self.switch_off = switch_off.subsample(2)
    self.switch_on = switch_on.subsample(2)
    self.vswitch_off = vswitch_off.subsample(2)
    self.vswitch_on = vswitch_on.subsample(2)

    self.dial_image = dial.resize((int(dial.size[0] * 1.15), int(dial.size[1] * 1.15)))
    self.dial = ImageTk.PhotoImage(self.dial_image.rotate(110, expand=True))

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

    self.tag_bind('CHAT_SWITCH', '<ButtonPress-1>', self.toggleChat)
    self.tag_bind('MODE_SWITCH', '<ButtonPress-1>', self.toggleMode)
    self.tag_bind('DIAL', '<B1-Motion>', self.handleDial)
    self.tag_bind('DIAL', '<ButtonRelease-1>', self.handleDialRelease)
