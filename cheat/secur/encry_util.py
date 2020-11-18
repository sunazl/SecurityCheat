import base64
import json
import time
from datetime import datetime

import rsa
from Crypto.Cipher import AES
from pyDes import des

from cheat.utils.log import log


class encry_util():
    def __init__(self):
        self.vi = "1308211992081479"
        self.key = 'gandiaoweixinheqq'
        self.des_key = b'KillAll!'
        self.pubkey_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.pubkey, self.privkey = rsa.newkeys(1024)
        log.info("加密初始化完成")
        log.info("公钥,私钥生成完毕")
        self.connection_key = {}
        self.user_pub_key = {}

    def aes_encrypt(self, data):
        pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        data = pad(data)
        cipher = AES.new(self.key.encode('utf8'), AES.MODE_CBC, self.vi.encode('utf8'))
        encryptedbytes = cipher.encrypt(data.encode('utf8'))
        encodestrs = base64.b64encode(encryptedbytes)
        enctext = encodestrs.decode('utf8')
        return enctext

    def aes_decrypt(self, data):
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
    def rsa_encrypt(self, str):
        content = str.encode("utf-8")
        # 公钥加密
        crypto = rsa.encrypt(content, self.pubkey)
        return (crypto, self.privkey)

    # rsa解密
    def rsa_decrypt_by_req(self, req):
        # 私钥解密
        decode = base64.b64decode(req['encry_data'])
        length = len(decode)
        result = ""
        for i in range(0, length, 128):
            tpl = decode[i:i + 128]
            privkey = self.get_connection_key()['privkey']
            result += str(rsa.decrypt(tpl, privkey), encoding="utf-8")
        return json.loads(result)

    # 获取公钥
    def get_pubkey(self):
        return self.pubkey

    # 获取私钥
    def get_privkey(self):
        return self.privkey

    # 获取登录密钥
    def get_connection_key(self):
        # 这里还要加判断  时间判断 用于修改
        create_time = time.time()
        if self.connection_key:
            return self.connection_key

        pubkey, privkey = rsa.newkeys(1024)
        self.connection_key = {"pubkey": pubkey, 'create_time': create_time, 'privkey': privkey}
        return self.connection_key

    # 密码解密
    def de_passwd(self, passwd):
        try:
            passwd_en = base64.b64decode(passwd)  # 使用base64解码为二进制
            k = des(self.des_key)
            passwd_de = k.decrypt(passwd_en).decode('utf-8').replace(" ", "")
        except Exception:
            # 非加密的密码直接返回
            return passwd
        return passwd_de

    # 密码加密
    def en_passwd(self, passwd):
        # 密钥
        while len(passwd) % 8 != 0:
            # 用空格来补全8位的长度,解密是需要去掉,同时密码不可包含空格(前端已经校验)
            passwd += ' '
        k = des(self.des_key)
        en = k.encrypt(passwd)
        passwd = str(base64.b64encode(en), 'utf-8')  # 改成字符串
        return passwd


    # 添加和获取用户公钥 pubkey为string注意转换格式
    def set_user_pub_key(self, user_id, user_pub_key):
        self.user_pub_key[user_id] = user_pub_key

    def get_user_pub_key(self, user_id):
        if self.user_pub_key.__contains__(user_id):
            return self.user_pub_key[user_id]


encry_util = encry_util()
