import tkinter as tk
import menu

from utils.fonts import _getFont
from chat import Chat

class Connect(tk.Frame):
  def __init__(self, root):
    self.frame = tk.Frame.__init__(self, root, background='black')
    self.root = root

    self.chatroom = tk.StringVar()
    self.username = tk.StringVar()
    self._isConnecting = False

    self._loadView()

  def connectChat(self, event=None):
    chatroom = self.chatroom.get()
    username = self.username.get()

    self._isConnecting = True

    self.root.chat = Chat()
    lobby = self.root.chat.connect(chatroom, username if username != '' else 'anon')

    self._isConnecting = False
    self.root.changeScreen(menu.Lobby)

  def _loadView(self):
    usernameField = tk.Entry(
      self,
      textvariable=self.username,
      bg='black',
      fg='white',
      highlightcolor='white',
      justify=tk.CENTER,
      state=tk.NORMAL if not self._isConnecting else 'readonly',
      font=_getFont('title2')
    )
    usernameLabel = tk.Label(
      self,
      text='USERNAME',
      bg='black',
      fg='white',
      font=_getFont('body')
    )
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
      text='ROOM ID',
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

    usernameLabel.place(x=500, y=205, anchor='center')
    usernameField.place(x=500, y=155, height=60, anchor='center')
    roomLabel.place(x=500, y=315, anchor='center')
    roomIdField.place(x=500, y=265, height=60, anchor='center')
    submit.place(x=500, y=405, height=60, width='430', anchor='center')
