import tkinter as tk
from utils.fonts import _getFont
from os import _exit

class Screen(tk.Frame):
  def __init__(self, root):
    self.frame = tk.Frame.__init__(self, root, width=300, height=600, background='black')
    self.root = root

    self.message = tk.StringVar()
    self.root.chat.listen(self.receiveMessage)

    self.root.protocol('WM_DELETE_WINDOW', self.handleWindowClose)

    self._loadView()

  def receiveMessage(self, data):
    self.messages.insert(tk.END, data)
    self.messages.yview(tk.END)

  def sendMessage(self, event=None):
    message = self.message.get()
    self.message.set('')
    data = self.root.chat._encode(message)

    self.root.chat.connection.asyncsend(data)

  def handleWindowClose(self):
    self.root.chat.disconnect()
    self.root.destroy()
    _exit(0)

  def _loadView(self):
    chatroom = tk.Label(
      self,
      text='{} [{}]'.format(self.root.chat.lobby, self.root.chat.user.name),
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
    self.messages = tk.Listbox(
      self,
      bg='black',
      fg='white',
      borderwidth=0,
      highlightthickness=0,
      font=_getFont('body')
    )

    inputField.bind('<Return>', self.sendMessage)

    chatroom.place(x=0, y=20, width=300)
    inputField.place(x=5, y=530, width=290, height=65)
    self.messages.place(x=5, y=60, width=290, height=450)

# class Screen(tk.Frame):  
#   def __init__(self, parent):
#     self.frame = tk.Frame.__init__(self, parent, background='white')
#     self.parent = parent

#     self.message = tk.StringVar()
#     self.message.set('Enter message here')

#     self.chat = Chat(self)
#     self.chat.prepareConnection();

#     self._loadView()
#     self.parent.protocol('WM_DELETE_WINDOW', self.handleClose);

#   def appendMessage(self, data):
#     self.msglist.insert(tk.END, data)

#   def handleSendPayload(self, event=None):
#     message = self.message.get()
#     self.chat.sendPayload(message)
#     self.message.set('')

#   def handleClose(self, event=None):
#     self.chat.closeConnection()
#     self.parent.destroy()
#     _exit(0)

#   def _loadView(self):
#     scrollbar = tk.Scrollbar(self)
#     self.msglist = tk.Listbox(self, height=15, width=50, yscrollcommand=scrollbar.set)
#     input_field = tk.Entry(self, textvariable=self.message)
#     send_btn = tk.Button(self, text='Send', command=self.handleSendPayload)

#     input_field.bind('<Return>', self.handleSendPayload)

#     scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#     self.msglist.pack(side=tk.LEFT, fill=tk.BOTH)
#     input_field.pack()
#     send_btn.pack()
