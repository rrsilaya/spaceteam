from socket import AF_INET, socket, SOCK_STREAM
from sys import stdin
from select import select

HOST = '202.92.144.45'
TCP_PORT = 80
UDP_PORT = 3003
BUFFER = 4096

class TcpConnection():
  def __init__(self):
    self.address = (HOST, TCP_PORT)
    self.active = False
    self._socket = socket(AF_INET, SOCK_STREAM)

    self._socket.connect(self.address)

  def receive(self, sender, receiver):
    self.active = True

    while self.active:
      try:
        infds, outfds, errfds = select([0, self._socket], [], [])
        
        for packet in infds:
          if packet == 0:
            data = sender()
            self._socket.send(data.SerializeToString())

            if data.type == 0:
              self.close()
          elif packet == self._socket:
            data = self._socket.recv(BUFFER)
            receiver(data)
      except:
        self.close()

  def send(self, data):
    self._socket.send(data.SerializeToString())

    res = self._socket.recv(BUFFER)
    return res

  def close(self):
    self.active = False
    self._socket.shutdown(1)
    self._socket.close()
