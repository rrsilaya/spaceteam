from socket import AF_INET, socket, SOCK_DGRAM
from threading import Thread

HOST = '127.0.0.1'
PORT = 3003
BUFFER = 4096

class UdpServer:
  def __init__(self):
    self.address = (HOST, PORT)

    self._socket = socket(AF_INET, SOCK_DGRAM)
    self._socket.bind(self.address)

    self.active = True

  def send(self, address, data):
    self._socket.sendto(data.SerializeToString(), address)

  def broadcast(self, room, data):
    payload = data.SerializeToString()

    for player in room:
      self._socket.sendto(payload, (player['ip_addr'], player['port']))

  def _receive(self):
    while self.active:
      # try:
        data, address = self._socket.recvfrom(BUFFER)

        self.recvCallback(data, address)
      # except Exception as e:
      #   print('An error occured')
      #   print(e)
      #   break

  def listen(self, recvCallback):
    self.recvCallback = recvCallback

    print('Server is listening to port %d\n' % PORT)
    Thread(target=self._receive).start()
