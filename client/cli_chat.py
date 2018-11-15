from chat.main import Chat
import sys

if __name__ == '__main__':
  chat = Chat()

  if input('Create a new lobby (Y/N)? ') == 'y':
    lobby = chat.createLobby(5)
  else:
    lobby = input('Lobby ID: ')

  username = input('Enter username: ')

  print('Connecting to lobby {}...'.format(lobby))
  print()
  chat.connect(lobby, username)
  chat.listen()
