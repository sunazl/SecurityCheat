'''
用于交换私钥,发送公钥
'''
import base64

from secur.encry_util import encry_util
from secur.exchange_privkey_util import exchange_util

'''
密钥交换流程:
user1 发起code申请,发送自己的公钥到服务器
user2 填写user1 的id 和code,验证成功后接收user1的公钥
启动监听线程:
user2 把通过user1公钥加密的私钥,及未加密的公钥发送至服务器,等待user1的私钥
user1 接收user2的公钥,发送自己通过user2公钥加密的私钥
user1,2储存好,私钥交换完毕
'''


def create_code(req):
    user_id = req['user_id']
    pubkey = req['pubkey']

    code = exchange_util.create_code(user_id)
    encry_util.set_user_pub_key(user_id, pubkey)

    return code


# user_id_my 请求聊天的一方
# user_id_other 生成聊天码的一方
cache_user_id = {}


def verify_code(req):
    user_id_my = req['user_id_my']
    user_id_other = req['user_id_other']
    code = req['code']
    result = exchange_util.verify_code(user_id_other, code)
    if result != "连接成功":
        return {'result': result}
    # 发起方的公钥
    cache_user_id[user_id_other] = user_id_my
    pubkey = encry_util.get_user_pub_key_str(user_id_other)
    return {'result': 'success', 'pubkey': pubkey, 'user_id_other': user_id_other}


# 接收用户的私钥和公钥
def send_my_key(req):
    encrypt_privkey = req['encrypt_privkey']
    user_id_my = req['user_id_my']
    # 加密方id
    user_id_other = req['user_id_other']
    pubkey = req['pubkey_str']

    exchange_util.set_privkey(user_id_other, user_id_my, encrypt_privkey)
    exchange_util.set_pubkey(user_id_other, user_id_my, pubkey)
    return 'sueecss'


# 获取对方私钥
def receive_other_privkey(req):
    user_id_my = req['user_id_my']
    user_id_other = req['user_id_other']
    privkey = exchange_util.get_privkey(user_id_my, user_id_other)
    if privkey == "未发起聊天":
        return {'result': privkey}
    return {"result": "success", "user_id_other": user_id_other, "privkey": privkey}


def waiting(req):
    user_id = req['user_id']
    if cache_user_id.__contains__(user_id):
        return {'result': 'success', 'user_id_other': cache_user_id[user_id],
                'other_pubkey': encry_util.get_user_pub_key_str(cache_user_id[user_id])}
    else:
        return {'result': 'waiting'}
