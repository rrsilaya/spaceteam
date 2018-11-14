from socket import AF_INET, socket, SOCK_STREAM
from sys import stdin

HOST = '202.92.144.45'
TCP_PORT = 80
UDP_PORT = 3003
BUFFER = 4096

class TcpConnection():
  def __init__(self):
    self.address = (HOST, TCP_PORT)
    self.active = True
    self._socket = socket(AF_INET, SOCK_STREAM)

    self._socket.connect(self.address)

  def receive(self, callback):
    while True:
      data = self._socket.recv(BUFFER)
      callback(data)

  def send(self, data):
    self._socket.send(data.SerializeToString())

    res = self._socket.recv(BUFFER)
    return res

  def close(self):
    self._socket.shutdown(1)
    self._socket.close()
