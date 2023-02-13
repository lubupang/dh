
'''
Copyright (c) <2021.1> <lubupang@gmail.com;lubupang@lubupang.com;464266236@qq.com>

"Anti 996" License Version 1.0 (Draft)



Permission is hereby granted to any individual or legal entity

obtaining a copy of this licensed work (including the source code,

documentation and/or related items, hereinafter collectively referred

to as the "licensed work"), free of charge, to deal with the licensed

work for any purpose, including without limitation, the rights to use,

reproduce, modify, prepare derivative works of, distribute, publish

and sublicense the licensed work, subject to the following conditions:



1. The individual or the legal entity must conspicuously display,

without modification, this License and the notice on each redistributed

or derivative copy of the Licensed Work.



2. The individual or the legal entity must strictly comply with all

applicable laws, regulations, rules and standards of the jurisdiction

relating to labor and employment where the individual is physically

located or where the individual was born or naturalized; or where the

legal entity is registered or is operating (whichever is stricter). In

case that the jurisdiction has no such laws, regulations, rules and

standards or its laws, regulations, rules and standards are

unenforceable, the individual or the legal entity are required to

comply with Core International Labor Standards.



3. The individual or the legal entity shall not induce, suggest or force

its employee(s), whether full-time or part-time, or its independent

contractor(s), in any methods, to agree in oral or written form, to

directly or indirectly restrict, weaken or relinquish his or her

rights or remedies under such laws, regulations, rules and standards

relating to labor and employment as mentioned above, no matter whether

such written or oral agreements are enforceable under the laws of the

said jurisdiction, nor shall such individual or the legal entity

limit, in any methods, the rights of its employee(s) or independent

contractor(s) from reporting or complaining to the copyright holder or

relevant authorities monitoring the compliance of the license about

its violation(s) of the said license.



THE LICENSED WORK IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,

EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF

MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM,

DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR

OTHERWISE, ARISING FROM, OUT OF OR IN ANY WAY CONNECTION WITH THE

LICENSED WORK OR THE USE OR OTHER DEALINGS IN THE LICENSED WORK.
'''
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto import Random
import random
import hashlib
from functools import reduce
import re
class Client:
    key=(0xe028064dc227ad0273410a6a771ac6e1afcb93018b56cdbec60ea82310208955c2d5f8b052f143366218d23c9915da21c477d5e67fd154556ae03d448ddb1153,2)    
    remotePublicNum=-1
    privateNum=-1
    publicNum=-1    
    def __init__(self):
        _r=int(random.random()*self.key[0])
        self.privateNum=_r
        self.publicNum=_mod(self.key[1],_r,self.key[0])
    def setRemotePublicNum(self,num):
        self.remotePublicNum=num
    def decrypt(self,enc):
        enc=enc.replace(' ','')
        p='([a-fA-F0-9]{16})+'
        if not re.fullmatch(p,enc):
            return ""
        return self.cipher.decrypt(enc)
    def encrypt(self,raw):
        return self.cipher.encrypt(raw)   
    @property 
    def ckey(self):
        assert self.remotePublicNum!=-1
        return _mod(self.remotePublicNum,self.privateNum,self.key[0])
    @property
    def cipher(self):
        return AESCipher(hex(self.ckey))
    @property
    def IsHandshaked(self):
        return self.remotePublicNum!=-1


class AESCipher:
    def __init__( self, key ):
        self.bs = 32
        self.key = bytes.fromhex(hashlib.sha256(key.encode()).hexdigest())

    def encrypt( self, raw ):
        content_padding = self._pad(raw).encode()
        iv = Random.new().read(AES.block_size)
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        encrypt_bytes = cipher.encrypt(content_padding)
        return (iv + encrypt_bytes).hex()

    def decrypt( self, enc ):
        enc=re.sub(r'[\r\n\t]','',enc)
        enc = bytes.fromhex(enc)
        iv = enc[:AES.block_size]
        enc = enc[AES.block_size:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypt_bytes = enc
        decrypt_bytes = cipher.decrypt(encrypt_bytes)
        return self._unpad(decrypt_bytes.decode('utf-8'))

    def _pad(self, s):
        return s + (self.bs - len(s.encode()) % self.bs) * chr(self.bs - len(s.encode()) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]





def _mod(a,b,c):
    '''
    优化a**b%c这玩意不优化不行啊
    ''' 
    d=[]
    binaryString=bin(b)[2:]
    
    r=len(binaryString)
    d=list(range(r))
    ds=[]
    for x in range(r):
        if x==0:
            
            d[x]=a%c
            
        else:
            d[x]=((d[x-1]%c )**2)%c
        if binaryString[x:x+1]=='1':
            ds.append(r-x-1)
    res=1
    for x in ds:
        res=(res*d[x])%c
    
    return res
