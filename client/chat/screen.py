import tkinter as tk
from utils.fonts import _getFont

class Screen(tk.Frame):
  def __init__(self, root):
    self.frame = tk.Frame.__init__(self, root, width=300, height=600, background='black')
    self.root = root

    self.message = tk.StringVar()

    if self.root.enableChat:
      self.root.chat.listen(self.receiveMessage)

    self._loadView()

  def receiveMessage(self, data, color='WHITE'):
    self.messages.config(state=tk.NORMAL)
    self.messages.insert(tk.END, data, color)
    self.messages.yview(tk.END)
    self.messages.config(state=tk.DISABLED)

  def sendMessage(self, event=None):
    message = self.message.get()
    self.message.set('')
    data = self.root.chat._encode(message)

    self.root.chat.connection.asyncsend(data)

  def _loadView(self):
    chatroom = tk.Label(
      self,
      text='CHAT DISABLED' if not self.root.enableChat else '{} [{}]'.format(
        self.root.chat.lobby,
        self.root.chat.user.name
      ),
      bg='black',
      fg='white',
      font=_getFont('title3')
    )
    inputField = tk.Entry(
      self,
      textvariable=self.message,
      bg='black',
      fg='white',
      highlightcolor='white',
      justify=tk.CENTER,
      font=_getFont('body')
    )
    self.messages = tk.Text(
      self,
      bg='black',
      fg='white',
      borderwidth=0,
      state=tk.DISABLED,
      highlightthickness=0,
      font=_getFont('body')
    )

    self.messages.tag_configure('WHITE', foreground='white')
    self.messages.tag_configure('RED', foreground='red')
    self.messages.tag_configure('GREEN', foreground='green')
    self.messages.tag_configure('YELLOW', foreground='yellow')

    chatroom.place(x=0, y=20, width=300)
    self.messages.place(x=5, y=60, width=290, height=450)

    inputField.bind('<Return>', self.sendMessage)
    inputField.place(x=5, y=530, width=290, height=65)
    inputField.focus()
