import tkinter as tk

from chat.screen import Screen as ChatScreen

class MainApplication(tk.Tk):
  def __init__(self):
    tk.Tk.__init__(self)
    self.title('Spaceteam')

    self._screen = None
    self.change_screen(ChatScreen)

  def change_screen(self, screen):
    next_screen = screen(self)

    if self._screen is not None:
      self._screen.destroy()

    self._screen = next_screen
    self._screen.pack(expand=1, fill=tk.BOTH)

if __name__ == '__main__':
  app = MainApplication()

  app.geometry('900x500')
  app.resizable(0, 0)

  app.mainloop()
