from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM
from sys import stdin, exit
from select import select
from threading import Thread

HOST = '202.92.144.45'
TCP_PORT = 80
UDP_PORT = 3003
BUFFER = 4096

class TcpConnection:
  def __init__(self):
    self.address = (HOST, TCP_PORT)
    self.active = False
    self._socket = socket(AF_INET, SOCK_STREAM)

    self._socket.connect(self.address)

  def receive(self, receiver):
    self.active = True

    while self.active:
      try:
        infds, outfds, errfds = select([0, self._socket], [], [])
        
        for packet in infds:
          if packet == self._socket:
            data = self._socket.recv(BUFFER)
            receiver(data)
      except ConnectionResetError:
        print('\nConnection reset by peer')
        self.active = False
        exit(1)
      except:
        self.close()

  def send(self, data):
    self._socket.send(data.SerializeToString())

    res = self._socket.recv(BUFFER)
    return res

  def asyncsend(self, data):
    self._socket.send(data.SerializeToString())

  def close(self):
    self.active = False
    self._socket.shutdown(1)
    self._socket.close()

class UdpConnection:
  def __init__(self, host='127.0.0.1'):
    self.address = (host, UDP_PORT)

    self._socket = socket(AF_INET, SOCK_DGRAM)
    self.active = True

  def send(self, data):
    self._socket.sendto(data.SerializeToString(), self.address)

  def _receive(self):
    while self.active:
      # try:
        data, address = self._socket.recvfrom(BUFFER)

        self.recvCallback(data)
      # except Exception as e:
      #   print('An error occured')
      #   print(e)
      #   break

  def listen(self, recvCallback):
    self.recvCallback = recvCallback
    Thread(target=self._receive).start()
