import tkinter as tk
from os import _exit
from chat.main import Chat

class Screen(tk.Frame):  
  def __init__(self, parent):
    self.frame = tk.Frame.__init__(self, parent, background='white')
    self.parent = parent

    self.message = tk.StringVar()
    self.message.set('Enter message here')

    self.chat = Chat(self)
    self.chat.prepareConnection();

    self._loadView()
    self.parent.protocol('WM_DELETE_WINDOW', self.handleClose);

  def appendMessage(self, data):
    self.msglist.insert(tk.END, data)

  def handleSendPayload(self, event=None):
    message = self.message.get()
    self.chat.sendPayload(message)
    self.message.set('')

  def handleClose(self, event=None):
    self.chat.closeConnection()
    self.parent.destroy()
    _exit(0)

  def _loadView(self):
    scrollbar = tk.Scrollbar(self)
    self.msglist = tk.Listbox(self, height=15, width=50, yscrollcommand=scrollbar.set)
    input_field = tk.Entry(self, textvariable=self.message)
    send_btn = tk.Button(self, text='Send', command=self.handleSendPayload)

    input_field.bind('<Return>', self.handleSendPayload)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    self.msglist.pack(side=tk.LEFT, fill=tk.BOTH)
    input_field.pack()
    send_btn.pack()
