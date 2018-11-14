from threading import Thread
from connection import TcpConnection

from proto.tcp_packet_pb2 import TcpPacket

class Chat():
  def __init__(self):#, gui):
    # self._gui = gui;
    self.connection = TcpConnection()
    self.packet = TcpPacket()

  def createLobby(self, maxPlayers, *args):
    payload = self.packet.CreateLobbyPacket()
    
    payload.type = self.packet.CREATE_LOBBY
    payload.max_players = maxPlayers

    if len(args) > 2:
      payload.lobby_id = args[2]

    lobby = self.connection.send(payload)
    payload.ParseFromString(lobby)

    return payload.lobby_id

  def connect(self, id, *args):
    payload = self.packet.ConnectPacket()

    payload.type = self.packet.CONNECT

    payload.lobby_id = id
    payload.player.name = args[2] if len(args) > 2 else 'anon'

    lobby = self.connection.send(payload)
    payload.ParseFromString(lobby)

    self.user = payload.player
    self.lobby = payload.lobby_id

    return payload.lobby_id

  def listen(self):
    self.stream = Thread(target=self.connection.receive, args=[self._parsePacket])
    self.stream.start()

  def sendChat(self, message):
    payload = self.packet.ChatPacket()

    payload.type = self.packet.CHAT
    payload.message = message
    payload.player.name = self.user.name
    payload.lobby_id = self.lobby

    chat = self.connection.send(payload)
    payload.ParseFromString(chat)

    return payload

  def getPlayerList(self):
    payload = self.packet.PlayerListPacket()

    payload.type = self.packet.PLAYER_LIST
    players = self.connection.send(payload)

    payload.ParseFromString(players)

    return payload

  def disconnect(self):
    payload = self.packet.DisconnectPacket()

    payload.type = self.packet.DISCONNECT
    payload.player.name = self.user.name
    payload.player.id = self.user.id

    disconnection = self.connection.send(payload)
    payload.ParseFromString(disconnection)

    return disconnection

  def _parse(type, packet):
    data = type()
    data.ParseFromString(packet)

    return data

  def _parsePacket(self, data):
    self.packet.ParseFromString(data)

    if self.packet.type == self.packet.DISCONNECT:
      return Chat._parse(self.packet.DisconnectPacket, data)
    elif self.packet.type == self.packet.CONNECT:
      data = Chat._parse(self.packet.ConnectPacket, data)
      print('{} has joined the chat'.format(data.player.name))
      return data#Chat._parse(self.packet.ConnectPacket, data)
    elif self.packet.type == self.packet.CHAT:
      data = Chat._parse(self.packet.ChatPacket, data)
      print('[{}]: {}'.format(data.player.name, data.message))
      return data#Chat._parse(self.packet.ChatPacket, data)
    elif self.packet.type == self.packet.PLAYER_LIST:
      return Chat._parse(self.packet.PlayerListPacket, data)
