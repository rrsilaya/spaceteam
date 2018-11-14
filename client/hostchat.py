from objects.tcp_packet_pb2 import TcpPacket
from objects.player_pb2 import Player

from connection import TcpConnection
from threading import Thread
from sys import stdout

connection = TcpConnection()
packet = TcpPacket()

chat_connection = packet.ConnectPacket()
chat_connection.type = packet.CONNECT

# Create new lobby
if input('Create new lobby (Y/N)? ') == 'y':
  packet.type = packet.CREATE_LOBBY
  lobby = packet.CreateLobbyPacket()
  lobby.type = packet.CREATE_LOBBY
  lobby.max_players = 5

  chatroom = connection.send(lobby.SerializeToString())
  lobby.ParseFromString(chatroom)
  lobby_id = lobby.lobby_id

  print('Lobby ID: {}'.format(lobby_id))

else:
  lobby_id = input('Enter lobby id: ')

username = input('Enter name: ')

# Connect to lobby
packet.type = packet.CONNECT
chat_connection.player.name = username
chat_connection.lobby_id = lobby_id

print('Loading chatroom {}...'.format(lobby_id))

connection.send(chat_connection.SerializeToString())

listpack = packet.PlayerListPacket()
chat_send = packet.ChatPacket()
chat_send.type = packet.CHAT

def parseData(data):
  packet.ParseFromString(data)

  if packet.type == packet.CONNECT:
    chat_connection.ParseFromString(data)
    print('{} has joined the chat'.format(chat_connection.player.name))
  elif packet.type == packet.CHAT:
    chat_send.ParseFromString(data)
    print('[{}] {}'.format(chat_send.player.name, chat_send.message))
  else:
    print('Packet received')

  print('CHAT >> ', sep='')
  stdout.flush()
  # print('[{}]: {}', chat.player, chat.message)

recv_thread = Thread(target=connection.receive, args=[parseData])
recv_thread.start()

chat_send.lobby_id = chat_connection.lobby_id
chat_send.player.name = username

listpack.type = packet.PLAYER_LIST

while True:
  reply = input('CHAT >> ')
  
  if (reply == 'lp'):
    recv = connection.send(listpack.SerializeToString())
    listpack.ParseFromString(recv)

    for player in listpack.player_list:
      print('{}'.format(player.name))
  else:
    chat_send.message = reply
    connection.send(chat_send.SerializeToString())

      # rcv.Parse
