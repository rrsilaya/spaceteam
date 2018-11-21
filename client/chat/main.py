import sys

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
    payload.player.name = args[0] if args else 'anon'

    self.user = payload.player
    self.lobby = payload.lobby_id
    self.prompt = '[CHAT:{}]> '.format(self.user.name)

    lobby = self.connection.send(payload)
    self.packet.ParseFromString(lobby)

    if self.packet.type == self.packet.CONNECT:
      payload.ParseFromString(lobby)
      return payload.lobby_id
    elif self.packet.type == self.packet.ERR_LDNE:
      payload = self.packet.ErrLdnePacket()
      payload.ParseFromString(lobby)

      print(payload.err_message)
      sys.exit(1)
    elif self.packet.type == self.packet.ERR_LFULL:
      payload = self.packet.ErrLfullPacket()
      payload.ParseFromString(lobby)

      print(payload.err_message)
      sys.exit(1)

  def listen(self, receiveCallback):
    self.receiveCallback = receiveCallback

    self.stream = Thread(target=self.connection.receive, args=[self._getInput, self._parsePacket])
    self.stream.start()

    print(self.prompt, end='', flush=True)

  def sendChat(self, message):
    payload = self.packet.ChatPacket()

    payload.type = self.packet.CHAT
    payload.message = message
    payload.player.name = self.user.name
    payload.lobby_id = self.lobby

    return payload

  def getPlayerList(self):
    payload = self.packet.PlayerListPacket()

    payload.type = self.packet.PLAYER_LIST
    return payload

  def disconnect(self):
    payload = self.packet.DisconnectPacket()

    payload.type = self.packet.DISCONNECT
    payload.player.name = self.user.name
    payload.player.id = self.user.id

    return payload

  def _parse(type, packet):
    data = type()
    data.ParseFromString(packet)

    return data

  def _parsePacket(self, data):
    self.packet.ParseFromString(data)

    if self.packet.type == self.packet.DISCONNECT:
      data = Chat._parse(self.packet.DisconnectPacket, data)
      print('\x1b[2K\x1b[1A')
      print('{} has left the chat room'.format(data.player.name))
      # return data
    elif self.packet.type == self.packet.CONNECT:
      data = Chat._parse(self.packet.ConnectPacket, data)
      print('\x1b[2K\x1b[1A')
      print('{} has joined the chat'.format(data.player.name))
      # return data#Chat._parse(self.packet.ConnectPacket, data)
    elif self.packet.type == self.packet.CHAT:
      data = Chat._parse(self.packet.ChatPacket, data)
      print('\x1b[2K\x1b[1A')
      print('{}: {}'.format(data.player.name, data.message))
      self.receiveCallback('{}: {}'.format(data.player.name, data.message))
      # return data#Chat._parse(self.packet.ChatPacket, data)
    elif self.packet.type == self.packet.PLAYER_LIST:
      data = Chat._parse(self.packet.PlayerListPacket, data)
      print('\x1b[2K\x1b[1A')

      print('PLAYERS:', end=' ')
      for player in data.player_list:
        print('[{}@{}]'.format(player.name, player.id), end=' ')
      print()
      # return Chat._parse(self.packet.PlayerListPacket, data)

    print(self.prompt, end='', flush=True)

  def _encode(self, stdin):
    if stdin == 'lp()':
      data = self.getPlayerList()
    elif stdin == 'exit()':
      data = self.disconnect()
    else:
      data = self.sendChat(stdin)

    return data

  def _getInput(self):
    stdin = input(self.prompt)
    
    if stdin == 'lp()':
      data = self.getPlayerList()
    elif stdin == 'exit()':
      data = self.disconnect()
    else:
      data = self.sendChat(stdin)

    return data
