import tkinter as tk

from utils.fonts import _getFont
from threading import Thread
from time import sleep

class WaitingRoom(tk.Canvas):
  def __init__(self, root):
    tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg='#111111')

    self.hold = 0
    self.isHold = False

    self._loadView()

  def incrementHold(self):
    self.create_rectangle(0, 335, 0, 339, fill='green', tags='LOADER')

    while self.isHold and self.hold < 40:
      sleep(0.05)
      self.hold += 1

      self.delete('LOADER')
      self.create_rectangle(0, 335, (self.hold / 40.0) * 700, 339, fill='green', tags='LOADER')

    if self.hold != 40:
      while self.hold > 0:
        sleep(0.01)
        self.hold -= 1
        self.delete('LOADER')
        self.create_rectangle(0, 335, (self.hold / 40.0) * 700, 339, fill='green', tags='LOADER')

  def toggleBeam_on(self, event=None):
    self.create_image(350, 450, image=self.beam_toggled, tags='BEAM_TOGGLED')
    
    self.isHold = True
    hold = Thread(target=self.incrementHold)
    hold.start()

  def toggleBeam_off(self, event=None):
    self.delete('BEAM_TOGGLED')
    self.isHold = False

  def exitLobby(self, event=None):
    print('Exit lobby')

  def _loadView(self):
    door_img = tk.PhotoImage(file='assets/elements/exitdoor.png')
    beam_img = tk.PhotoImage(file='assets/elements/beam.png')
    beam_toggled_img = tk.PhotoImage(file='assets/elements/beam-toggled.png')
    floor_img = tk.PhotoImage(file='assets/elements/lobby-floor.png')
    wallpaper_img = tk.PhotoImage(file='assets/elements/lobby-wallpaper.png')

    player1_img = tk.PhotoImage(file='assets/elements/player.png')

    self.door = door_img.zoom(3).subsample(2)
    self.beam = beam_img
    self.beam_toggled = beam_toggled_img
    self.floor = floor_img.zoom(3).subsample(2)
    self.wallpaper = wallpaper_img

    self.avatars = [player1_img]
    self.avatars = [a.zoom(3).subsample(2) for a in self.avatars]

    # Wallpaper
    for y in range(11):
      for x in range(6):
        self.create_image(x * 128, y * 30, image=self.wallpaper, anchor=tk.NW)

    # Floor
    for x in range(5):
      self.create_image(x * 192, 310, image=self.floor)

    # Players
    for player in range(5):
      self.create_image(230 + (player * 80), 285, image=self.avatars[player % len(self.avatars)])
      
    self.create_image(80, 280, image=self.door, tags='DOOR')
    self.create_image(350, 450, image=self.beam, tags='BEAM')
    self.create_rectangle(50, 195, 110, 223, fill='green', outline='white')
    self.create_text(83, 210, font=_getFont('body3'), text='EXIT', fill='white')

    self.tag_bind('BEAM', '<ButtonPress-1>', self.toggleBeam_on)
    self.tag_bind('BEAM', '<ButtonRelease-1>', self.toggleBeam_off)
    self.tag_bind('DOOR', '<ButtonPress-1>', self.exitLobby)
