from utils import Client
import re
c=Client()
while not c.IsHandshaked:
    print("开始进行TLS握手")
    r=c.publicNum
    print("你的公开数字是")
    print(r)
    print("请发送给对方,然后输入对方发送的公开数字")
    a=input()
    try:
        _=int(a)
        c.setRemotePublicNum(_)
        print("握手成功")
    except:
        pass

e=False
while not e:
    print("1.加密我发消息")
    print("2.解密对方程序")
    print("0.退出本程序")
    a=input()
    a=a.replace(' ','')
    try:
        _=int(a)
        if _ not in [0,1,2]:
            print("只能输入0或者1或者2")
        else:
            if _==0:
                e=True
                break
            if _==1:
                print("输入你要发送的消息")
                a=input()
                try:
                    print("你加密后的文本为:")
                    print(c.encrypt(a))
                    print("注意是发送加密后的文本给对方")
                except:
                    pass
            if _==2:
                print("输入对方的加密后的文本")
                a=input()
                res=c.decrypt(a)
                if res=="":
                    print("密文格式不正确")
                else:
                    print("对方实际内容为:")
                    print(res)

    except:
        print("只能输入0或者1或者2")
