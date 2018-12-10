import tkinter as tk
import menu

from os import _exit

class MainApplication(tk.Tk):
  def __init__(self):
    tk.Tk.__init__(self)
    self.title('Spaceteam')
    self.protocol('WM_DELETE_WINDOW', self.handleWindowClose)

    self.chat = None
    self.enableChat = True
    self.gameConnection = None
    self.gameRoom = None

    self._screen = None
    self.changeScreen(menu.Main)

  def handleWindowClose(self):
    self.closeGameConnection()

    self.destroy()
    _exit(0)

  def closeGameConnection(self):
    if self.gameConnection is not None:
      packet = self.udpPacket
      payload = packet.DisconnectPacket()
      payload.type = packet.DISCONNECT

      self.gameConnection.send(payload)

  def changeScreen(self, screen):
    next = screen(self)

    if self._screen is not None:
      self._screen.destroy()

    self._screen = next
    self._screen.pack(expand=1, fill=tk.BOTH)

if __name__ == '__main__':
  app = MainApplication()

  app.geometry('1000x600')
  app.resizable(0, 0)

  app.mainloop()
