import tkinter as tk
from utils.fonts import _getFont

class Ship(tk.Canvas):
  def __init__(self, root):
    tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg='black')
    self.root = root

    self._loadView()

  def _loadView(self):
    ship = tk.PhotoImage(file='assets/elements/ship-small.png')
    instruction = tk.PhotoImage(file='assets/elements/instruction.png')
    timer_empty = tk.PhotoImage(file='assets/elements/timer-empty.png')

    self.ship = ship
    self.instruction = instruction.zoom(3).subsample(2)
    self.timer_empty = timer_empty.zoom(3).subsample(2)

    self.create_rectangle(0, 0, 700, 100, fill='blue', outline='')
    self.create_image(400, 50, image=self.ship, tags='SHIP')

    # Instruction
    for distance in range(8):
      self.create_image(distance * 95, 100, image=self.instruction, anchor=tk.NW)

    self.create_image(0, 195, image=self.timer_empty, anchor=tk.NW)
    self.create_image(480, 195, image=self.timer_empty, anchor=tk.NW)
    self.create_text(30, 150, text='▶  Engage Elgenthrottle', fill='white', font=_getFont('heading'), anchor=tk.W)