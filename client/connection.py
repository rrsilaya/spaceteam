from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

HOST = 'localhost'
TCP_PORT = 3002
UDP_PORT = 3003
BUFFER = 1024

class TcpConnection():
  def __init__(self):
    self.address = (HOST, TCP_PORT)
    self.active = True
    self._socket = socket(AF_INET, SOCK_STREAM)

    self._socket.connect(self.address)

  def receive(self, callback):
    while True:
      try:
        data = self._socket.recv(BUFFER).decode('utf8')
        callback(data)
      except OSError:
        break

  def send(self, data):
    self._socket.send(bytes(data, 'utf8'))

  def close(self):
    self._socket.shutdown(1)
    self._socket.close()
