#/usr/bin/env python
# -*- coding: utf-8 -*-
import rsa
import sys
import base64

# 打印 python 版本 与 windows 系统编码
print("---- 1 ----")
print(sys.version)
print(sys.getdefaultencoding())
print(sys.getfilesystemencoding())

# 先生成一对密钥，然后保存.pem格式文件，当然也可以直接使用
print("---- 2 ----")
(pubkey, privkey) = rsa.newkeys(1024)
pub = pubkey.save_pkcs1()
print(type(pub))
pubfile = open('public.pem','w+')
pubfile.write(pub.decode('utf-8'))
pubfile.close()

print("---- 3 ----")
pri = privkey.save_pkcs1()
print(type(pri))
prifile = open('private.pem','w+')
prifile.write(pri.decode('utf-8'))
prifile.close()

# load公钥和密钥
print("---- 4 ----")
message = 'dPabdbGDpFTrwwgydVafdlsadlfsal%46645645s'
print('message:',type(message))
with open('public.pem') as publickfile:
    p = publickfile.read()
    print(type(p))
    pubkey = rsa.PublicKey.load_pkcs1(p.encode('utf-8'))
with open('private.pem') as privatefile:
    p = privatefile.read()
    print(type(p))
    privkey = rsa.PrivateKey.load_pkcs1(p.encode('utf-8'))

# 用公钥加密、再用私钥解密
crypto = rsa.encrypt(message.encode('utf-8'),pubkey)
print(crypto)

print("---- 5 ----")
print('crypto:',type(crypto))
print('cry_base64:',base64.encodestring(crypto))
print('cry_base64_utf8:',base64.encodestring(crypto).decode('utf-8'))
# 保存到本地文件
cry_file = open('cry_file.txt','w+')
cry_file.write(base64.encodestring(crypto).decode('utf-8'))
cry_file.close()

print("---- 6 ----")
# 从本地文件读取
cry_file = open('cry_file.txt','r')
cry_text = ''
for i in cry_file.readlines():
    cry_text += i

print('cry_text_type:',type(cry_text))
print('cry_text:',cry_text)
print('cry_base64:',cry_text.encode('utf-8'))
crypto_tra = base64.decodestring(cry_text.encode('utf-8'))

print("---- 7 ----")
assert crypto == crypto_tra
print(crypto)

print("---- 8 ----")
plaintext = rsa.decrypt(crypto,privkey)
assert  message == plaintext.decode('utf-8')
print(plaintext.decode('utf-8'))