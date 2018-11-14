from chat.main import Chat
import sys

if __name__ == '__main__':
  chat = Chat()

  if input('Create a new lobby (Y/N)? ') == 'y':
    lobby = chat.createLobby(5)
  else:
    lobby = input('Lobby ID: ')

  username = input('Enter username: ')

  print('Connecting with lobby {}...'.format(lobby))
  print()
  chat.connect(lobby, username)
  chat.listen()

  while True:
    sys.stdout.flush()
    msg = input('CHAT:{} > '.format(username))

    if msg == 'lp()':
      res = chat.getPlayerList()
    elif msg == 'exit()':
      res = chat.disconnect()
      break
    else:
      res = chat.sendChat(msg)

    # print(res)