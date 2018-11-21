import tkinter as tk
import menu

from utils.fonts import _getFont
from chat import Chat

class Connect(tk.Frame):
  def __init__(self, root):
    self.frame = tk.Frame.__init__(self, root, background='black')
    self.root = root

    self.chatroom = tk.StringVar()
    self._isConnecting = False

    self._loadView()

  def connectChat(self, event=None):
    chatroom = self.chatroom.get()

    self._isConnecting = True

    self.root.chat = Chat()
    lobby = self.root.chat.connect(chatroom)

    self._isConnecting = False
    self.root.changeScreen(menu.Lobby)

  def _loadView(self):
    inputField = tk.Entry(
      self,
      textvariable=self.chatroom,
      bg='black',
      fg='white',
      highlightcolor='white',
      justify=tk.CENTER,
      state=tk.NORMAL if not self._isConnecting else 'readonly',
      font=_getFont('title2')
    )
    label = tk.Label(
      self,
      text='ENTER ROOM ID' if not self._isConnecting else 'CONNECTING...',
      bg='black',
      fg='white',
      font=_getFont('body')
    )

    inputField.bind('<Return>', self.connectChat)

    label.place(x=500, y=330, anchor='center')
    inputField.place(x=500, y=280, height=60, anchor='center')
