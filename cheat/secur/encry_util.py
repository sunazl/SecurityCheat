import base64

import rsa
from Crypto.Cipher import AES

from utils.log import log


class encry_util():
    def __init__(self):
        self.vi = "1308211992081479"
        self.key = 'gandiaoweixinheqq'
        self.pubkey, self.privkey = rsa.newkeys(512)
        log.info("加密初始化完成")
        log.info("公钥,私钥生成完毕")

    def AES_Encrypt(self, data):
        pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        data = pad(data)
        cipher = AES.new(self.key.encode('utf8'), AES.MODE_CBC, self.vi.encode('utf8'))
        encryptedbytes = cipher.encrypt(data.encode('utf8'))
        encodestrs = base64.b64encode(encryptedbytes)
        enctext = encodestrs.decode('utf8')
        return enctext

    def AES_Decrypt(self, data):
        data = data.encode('utf8')
        encodebytes = base64.decodebytes(data)
        # 将加密数据转换位bytes类型数据
        cipher = AES.new(self.key.encode('utf8'), AES.MODE_CBC, self.vi.encode('utf8'))
        text_decrypted = cipher.decrypt(encodebytes)
        unpad = lambda s: s[0:-s[-1]]
        text_decrypted = unpad(text_decrypted)
        # 去补位
        text_decrypted = text_decrypted.decode('utf8')
        return text_decrypted

    # rsa加密
    def rsaEncrypt(self, str):
        content = str.encode("utf-8")
        # 公钥加密
        crypto = rsa.encrypt(content, self.pubkey)
        return (crypto, self.privkey)

    # rsa解密
    def rsaDecrypt(self, str):
        # 私钥解密
        content = rsa.decrypt(str, self.privkey)
        con = content.decode("utf-8")
        return con

    def get_pubkey(self):
        return self.pubkey

    def get_privkey(self):
        return self.privkey


encry_util = encry_util()
