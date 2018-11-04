from threading import Thread
from connection import TcpConnection

class Chat():
  def __init__(self, gui):
    self._gui = gui;

    self.connection = TcpConnection()
    self.prepareConnection()

  def receivePayload(self, data):
    self._gui.appendMessage(data)

  def sendPayload(self, data):
    self.connection.send(data)

  def prepareConnection(self):
    self.recvThread = Thread(target=self.connection.receive, args=[self.receivePayload])
    self.recvThread.start()

  def closeConnection(self):
    self.connection.close()
