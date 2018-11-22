import tkinter as tk
import menu

from utils.fonts import _getFont
from chat import Chat

class Connect(tk.Frame):
  def __init__(self, root):
    self.frame = tk.Frame.__init__(self, root, background='black')
    self.root = root

    self.chatroom = tk.StringVar()
    self.chatroom.trace('w', self._handleInputField)
    self._isConnecting = False

    self._loadView()

  def connectChat(self, event=None):
    chatroom = self.chatroom.get()
    username = self.root.username

    self._isConnecting = True

    if not self.root.chat:
      self.root.chat = Chat()
    lobby = self.root.chat.connect(chatroom, username)

    self._isConnecting = False
    self.root.changeScreen(menu.Lobby)

  def _handleInputField(self, *args):
    value = self.chatroom.get()
    limit = 10

    self.chatroom.set(value.upper())
    value = value.upper()

    if len(value) > limit:
      self.chatroom.set(value[:limit])

  def _loadView(self):
    roomIdField = tk.Entry(
      self,
      textvariable=self.chatroom,
      bg='black',
      fg='white',
      highlightcolor='white',
      justify=tk.CENTER,
      state=tk.NORMAL if not self._isConnecting else 'readonly',
      font=_getFont('title2')
    )
    roomLabel = tk.Label(
      self,
      text='ENTER ROOM ID',
      bg='black',
      fg='white',
      font=_getFont('body')
    )
    submit = tk.Button(
      self,
      text='CONNECT',
      bg='black',
      fg='white',
      command=self.connectChat,
      font=_getFont('title2')
    )

    roomLabel.place(x=500, y=285, anchor='center')
    roomIdField.place(x=500, y=235, height=60, anchor='center')
    submit.place(x=500, y=345, height=60, width='430', anchor='center')

    roomIdField.focus()
    roomIdField.bind('<Return>', self.connectChat)
