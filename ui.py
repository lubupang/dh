try:
    import tkinter as Tkinter
    from tkinter.scrolledtext import ScrolledText
except ImportError:
    Tkinter = None
from utils import Client
if Tkinter:
    class NativeMessagingWindow(Tkinter.Frame):
        def __init__(self):
            self.c = Client()
            Tkinter.Frame.__init__(self)
            self.pack()
            self.toptext = Tkinter.Text(self)
            self.toptext.grid(row=0, column=0, padx=10, pady=10, columnspan=3)
            self.toptext.insert(Tkinter.END,"我的握手信息:\n")
            self.toptext.insert(Tkinter.END,str(self.c.publicNum)+'\n')
                       
            self.toptext.config(state=Tkinter.DISABLED, height=10, width=50)
            self.scrolledtext = ScrolledText(self)
            self.scrolledtext.grid(row=1, column=0, padx=10, pady=10, columnspan=3)
            self.scrolledtext.config(state=Tkinter.DISABLED, height=30, width=50)

            self.messageContent = Tkinter.StringVar()
            self.sendEntry = Tkinter.Entry(
                self, textvariable=self.messageContent)
            self.sendEntry.grid(row=2, column=0, padx=10, pady=10)
            self.initButton = Tkinter.Button(
                self, text="握手",command=self.oninit)
            self.initButton.grid(row=2, column=1, padx=10, pady=10, columnspan=2)
            self.text = Tkinter.Text(self)
            self.text.grid(row=3, column=0, padx=10, pady=10, columnspan=3)
            self.text.config(state=Tkinter.DISABLED, height=10, width=40)
            self.log("把最上面握手信息复制给对方")
            self.log("在下面输入框贴入对方的握手信息,然后点击握手")
        def oninit(self):
            try:
                text = self.messageContent.get()
                _ = int(text)
                self.c.setRemotePublicNum(_)
                self.initButton.destroy()
                self.sendButton = Tkinter.Button(
                    self, text="加密", command=self.onSend)
                self.receiveButton = Tkinter.Button(
                    self, text="解密", command=self.onReceive)
                self.sendButton.grid(row=2, column=1, padx=10, pady=10)
                self.receiveButton.grid(row=2, column=2, padx=10, pady=10)
                self.messageContent.set("")
                self.clearlog()
                self.changeInfo("握手成功(点击要发送的信息发送,或者点击要解密的信息解密即可聊天)")
                self.toptext.config(state=Tkinter.NORMAL, height=10, width=40)
                self.toptext.insert(Tkinter.END,"发送对方消息前,新通过此处加密然后把加密后的信息发送给对方:\n")
                self.toptext.insert(Tkinter.END,"收到消息后,通过此处解密阅读解密后的信息即可:\n")
                self.toptext.insert(Tkinter.END,"微信聊天窗口是全程看不到明文内容的:\n")
                self.toptext.config(state=Tkinter.DISABLED, height=10, width=40)
            except:
                pass

        def onSend(self):
            text = self.messageContent.get()
            _=self.c.encrypt(text)
            self.changeInfo(f"加密后的信息: \n{_}")
            self.log('我: %s' % text)
            self.messageContent.set("")

        def onReceive(self):
            text = self.messageContent.get()
            try:
                _=self.c.decrypt(text)
            except:
                self.changeInfo(rf"解密失败,请重新握手,可能是握手数字复制不全.确保对方和你均只复制了握手信息的数字部分")
            self.changeInfo(f"解密后的信息: \n{_}")
            self.log('TA: %s' % _)
            self.messageContent.set("")
        def changeInfo(self,info):
            self.text.config(state=Tkinter.NORMAL)
            self.text.delete("1.0",Tkinter.END)
            self.text.insert(Tkinter.END, info + "\n")
            self.text.config(state=Tkinter.DISABLED)

        def log(self, message):
            self.scrolledtext.config(state=Tkinter.NORMAL)
            self.scrolledtext.insert(Tkinter.END, message + "\n")
            self.scrolledtext.config(state=Tkinter.DISABLED)
        def clearlog(self):
            self.scrolledtext.config(state=Tkinter.NORMAL)
            self.scrolledtext.delete("1.0",Tkinter.END)
            self.scrolledtext.config(state=Tkinter.DISABLED)
def main():
    if not Tkinter:
        print("启动失败 没有tkinter")
    main_window = NativeMessagingWindow()
    main_window.master.title('简易聊天加密工具')
    main_window.mainloop()

if __name__=="__main__":
    main()
