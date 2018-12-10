import tkinter as tk
import menu
import chat

from game import WaitingRoom

class Lobby(tk.Frame):
  def __init__(self, root):
    self.frame = tk.Frame.__init__(self, root, background='black')
    self.root = root

    self.enableChat = self.root.enableChat
    self.udpPacket = self.root.udpPacket
    self.gameConnection = self.root.gameConnection

    self.gameData = { 'screen': 'LOBBY', 'room': self.root.gameRoom }
    self._loadView()
    self.gameConnection.listen(self.streamParser)

  def parsePacket(type, packet):
    data = type()
    data.ParseFromString(packet)

    return data

  def streamParser(self, data):
    p = self.udpPacket
    p.ParseFromString(data)

    if p.type == p.GAME_STATE:
      # Change in game state
      data = Lobby.parsePacket(p.GameStatePacket, data)

      if data.update == p.GameStatePacket.CONNECT or data.update == p.GameStatePacket.DISCONNECT:
        self.gameData['players'] = data.player_count

        if self.gameData['screen'] == 'LOBBY' and 'renderPlayers' in self.gameData:
          self.gameData['renderPlayers'](data.player_count)

  def changeGameScreen(self, screen):
    before = self.game
    before.destroy()

    self.game = screen(self)
    self.game.pack(side=tk.LEFT)

  def exitLobby(self):
    if self.enableChat and self.root.chat:
      self.root.chat.disconnect()
      self.root.chat = None
    
    self.root.closeGameConnection()
    self.root.enableChat = True
    self.chatbox.destroy()
    self.game.destroy()
    self.root.changeScreen(menu.Main)

  def _loadView(self):
    self.chatbox = chat.Screen(self.root)
    self.game = WaitingRoom(self)

    self.chatbox.pack(side=tk.RIGHT)
    self.game.pack(side=tk.LEFT)
