import random
import time


class exchange():
    def __init__(self):
        # userid 1
        self.code = {}
        self.privkey_user = {}

    def create_code(self, user_id):
        now = time.time()
        if self.code.__contains__(user_id) and -now - float(self.code[user_id].split(";")[1])  < 250:
            return self.code[user_id].split(";")[0]
        code = ""
        for i in range(0, 4):
            code += str(random.randint(0, 9))

        self.code[user_id] = code + ";" + str(now)
        return code

    def verify_code(self, user_id, code):
        now = time.time()
        if self.code.__contains__(user_id):
            split = self.code[user_id].split(';')
            code_ = split[0]
            create_time = split[1]
            if code_ != code:
                return '输入错误,或者别人压根就不想和你聊天'
            elif now - float(create_time) > 300:
                return '验证码已过期'
            elif code_ == code and now - float(create_time) <= 300:
                return '连接成功'
            else:
                return '未知错误,反正就是没连上'


        else:
            return  '输入错误,或者别人压根就不想和你聊天'

    # 该私钥是根据用户的公钥的加密后的结果
    # user_id_my 用户  user_id_other 目标端 privkey 根据 用户公钥加密的目标用户私钥
    def set_privkey(self, user_id_my, user_id_other, privkey):
        self.privkey_user[user_id_my] = {user_id_other: privkey}

    def get_privkey(self, user_id_my, user_id_other):

        if self.privkey_user.__contains__(user_id_my):
            id_prk = self.privkey_user[user_id_my]
            if id_prk.__contains__(user_id_other):
                return id_prk[user_id_other]
            else:
                return '未发起聊天'
        else:
            return '未发起聊天'


exchange_util = exchange()
